import os
import numpy as np
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from app.models import db, Persona, Log

class GeminiService:
    def __init__(self):
        # Configuración de API
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY no está configurada en las variables de entorno")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Inicializar vector store
        self.vector_store = None
        self.initialize_vector_store()

        # Configuración del sistema
        self.system_prompt = """
        Eres un asistente que ayuda a gestionar datos personales. Puedes responder preguntas sobre
        las personas registradas en la base de datos. La base de datos tiene una tabla 'persona' con
        campos: id_persona, primer_nombre, segundo_nombre, apellidos, fecha_nacimiento, genero,
        correo, celular, tipo_documento, foto. También hay una tabla 'log' que registra acciones.
        """

    def initialize_vector_store(self):
        """Inicializa el almacén de vectores con los datos de la base de datos"""
        try:
            # Obtener todos los datos de personas
            personas = Persona.query.all()
            persona_docs = []

            # Crear documentos para cada persona
            for persona in personas:
                persona_dict = persona.to_dict()
                content = f"""
                ID: {persona_dict['id_persona']}
                Nombre: {persona_dict['primer_nombre']} {persona_dict.get('segundo_nombre', '')} {persona_dict['apellidos']}
                Fecha de nacimiento: {persona_dict['fecha_nacimiento']}
                Género: {persona_dict['genero']}
                Correo: {persona_dict['correo']}
                Celular: {persona_dict['celular']}
                Tipo de documento: {persona_dict['tipo_documento']}
                """

                # Crear documento con metadatos
                doc = Document(
                    page_content=content,
                    metadata={
                        "id_persona": persona_dict['id_persona'],
                        "tipo": "persona"
                    }
                )
                persona_docs.append(doc)

            # Obtener logs recientes
            logs = Log.query.order_by(Log.fecha.desc()).limit(50).all()
            log_docs = []

            # Crear documentos para cada log
            for log in logs:
                content = f"""
                ID Log: {log.id_log}
                Acción: {log.accion}
                Fecha: {log.fecha.strftime('%Y-%m-%d %H:%M:%S')}
                ID Persona: {log.id_persona}
                """

                # Crear documento con metadatos
                doc = Document(
                    page_content=content,
                    metadata={
                        "id_log": log.id_log,
                        "tipo": "log"
                    }
                )
                log_docs.append(doc)

            # Combinar todos los documentos
            all_docs = persona_docs + log_docs

            # Crear el almacén de vectores
            if all_docs:
                self.vector_store = FAISS.from_documents(all_docs, self.embeddings)
                print(f"Vector store inicializado con {len(all_docs)} documentos")
            else:
                print("No se encontraron documentos para inicializar el vector store")

        except Exception as e:
            print(f"Error al inicializar vector store: {str(e)}")
            # Crear un vector store vacío como fallback
            self.vector_store = FAISS.from_documents([Document(page_content="No data")], self.embeddings)

    def refresh_vector_store(self):
        """Actualiza el almacén de vectores con datos frescos"""
        self.initialize_vector_store()
        return "Vector store actualizado correctamente"

    def semantic_search(self, query, k=3):
        """Realiza una búsqueda semántica en el vector store"""
        if not self.vector_store:
            return []

        try:
            results = self.vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Error en búsqueda semántica: {str(e)}")
            return []

    def query_database(self, query_type, filters=None):
        """Consulta la base de datos según el tipo de consulta y filtros"""
        if query_type == "all_personas":
            personas = Persona.query.all()
            return [p.to_dict() for p in personas]

        elif query_type == "persona_by_id" and filters and 'id' in filters:
            persona = Persona.query.filter_by(id_persona=filters['id']).first()
            return persona.to_dict() if persona else None

        elif query_type == "personas_by_name" and filters and 'name' in filters:
            personas = Persona.query.filter(
                Persona.primer_nombre.ilike(f"%{filters['name']}%") |
                Persona.apellidos.ilike(f"%{filters['name']}%")
            ).all()
            return [p.to_dict() for p in personas]

        elif query_type == "recent_logs":
            logs = Log.query.order_by(Log.fecha.desc()).limit(10).all()
            return [{
                'id_log': log.id_log,
                'accion': log.accion,
                'fecha': log.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                'id_persona': log.id_persona
            } for log in logs]

        return None

    def process_query(self, user_query):
    	"""Procesa una consulta en lenguaje natural usando RAG"""
    	self.refresh_vector_store()

    	# Paso 1: Realizar búsqueda semántica
    	semantic_results = self.semantic_search(user_query)

    	# Extraer el contenido relevante de los resultados
    	retrieved_contexts = []
    	for doc in semantic_results:
        	retrieved_contexts.append(doc.page_content)

    	# Paso 2: Como respaldo, también realizar la búsqueda estructurada original
    	# Determinar qué tipo de consulta es
    	query_analysis = self.model.generate_content(
        	f"{self.system_prompt} \n \nAnaliza esta consulta: '{user_query}'. ¿Qué tipo de información está solicitando el usuario? "
        	"Responde con una de estas opciones: 'all_personas', 'persona_by_id', 'personas_by_name', 'recent_logs', 'general'. "
        	"Si necesita un ID específico, responde con 'persona_by_id:ID'. "
        	"Si busca por nombre, responde con 'personas_by_name:NOMBRE'.").text

    	# Extraer datos según el análisis
    	structured_data = None
    	if "all_personas" in query_analysis:
        	structured_data = self.query_database("all_personas")
    	elif "persona_by_id" in query_analysis:
        	try:
            		id_part = query_analysis.split(":")[1].strip()
            		id_value = int(''.join(filter(str.isdigit, id_part)))
            		structured_data = self.query_database("persona_by_id", {"id": id_value})
        	except:
            		structured_data = None
    	elif "personas_by_name" in query_analysis:
        	try:
            		name_part = query_analysis.split(":")[1].strip()
            		structured_data = self.query_database("personas_by_name", {"name": name_part})
        	except:
            		structured_data = None
    	elif "recent_logs" in query_analysis:
        	structured_data = self.query_database("recent_logs")

    	# Paso 3: Combinar resultados de ambos métodos
    	context = ""

    	# Añadir resultados de búsqueda semántica
    	if retrieved_contexts:
        	context += "Resultados de búsqueda semántica: \n"
        	for i, ctx in enumerate(retrieved_contexts, 1):
            		context += f"Resultado {i}: \n {ctx} \n \n"

    	# Añadir resultados de búsqueda estructurada
    	if structured_data:
        	context += f" \n Resultados de búsqueda estructurada: \n {structured_data} \n"

    	if not context:
        	context = "No se encontraron datos relevantes."

    	# Paso 4: Generar respuesta con el LLM usando el contexto combinado
    	prompt = f"""
    	{self.system_prompt}

    	Usa la siguiente información para responder a la consulta del usuario. Si la información no es suficiente,
    	indica que no tienes suficientes datos para responder. Responde siempre en español y de manera natural y conversacional.

    	Contexto: {context}

    	Consulta del usuario: {user_query}
    	"""

    	response = self.model.generate_content(prompt)

    	return response.text
