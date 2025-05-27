import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from models import db, Persona, Log

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY no está configurada en las variables de entorno")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

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
        """Procesa una consulta en lenguaje natural y devuelve una respuesta"""
        # Analizar la consulta para determinar qué datos necesitamos
        system_prompt = """
        Eres un asistente que ayuda a gestionar datos personales. Puedes responder preguntas sobre
        las personas registradas en la base de datos. La base de datos tiene una tabla 'persona' con
        campos: id_persona, primer_nombre, segundo_nombre, apellidos, fecha_nacimiento, genero,
        correo, celular, tipo_documento, foto. También hay una tabla 'log' que registra acciones.
        """

        # Determinar qué tipo de consulta es
        query_analysis = self.model.generate_content([
            system_prompt,
            f"Analiza esta consulta: '{user_query}'. ¿Qué tipo de información está solicitando el usuario? "
            "Responde con una de estas opciones: 'all_personas', 'persona_by_id', 'personas_by_name', 'recent_logs', 'general'. "
            "Si necesita un ID específico, responde con 'persona_by_id:ID'. "
            "Si busca por nombre, responde con 'personas_by_name:NOMBRE'."
        ]).text

        # Extraer datos según el análisis
        data = None
        if "all_personas" in query_analysis:
            data = self.query_database("all_personas")
        elif "persona_by_id" in query_analysis:
            try:
                id_part = query_analysis.split(":")[1].strip()
                id_value = int(''.join(filter(str.isdigit, id_part)))
                data = self.query_database("persona_by_id", {"id": id_value})
            except:
                data = None
        elif "personas_by_name" in query_analysis:
            try:
                name_part = query_analysis.split(":")[1].strip()
                data = self.query_database("personas_by_name", {"name": name_part})
            except:
                data = None
        elif "recent_logs" in query_analysis:
            data = self.query_database("recent_logs")

        # Generar respuesta con el LLM
        context = f"Datos disponibles: {data}" if data else "No se encontraron datos relevantes."
        response = self.model.generate_content([
            system_prompt,
            {"role": "user", "parts": [user_query]},
            {"role": "model", "parts": ["Analizando tu consulta..."]},
            {"role": "user", "parts": [context]}
        ])

        return response.text
