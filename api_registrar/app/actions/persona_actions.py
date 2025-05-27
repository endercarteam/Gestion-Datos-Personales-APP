from app.models import db, Persona, Log
from datetime import datetime

class PersonaActions:
    @staticmethod
    def registrar_persona(data):
        try:
            # Crear nueva persona
            nueva_persona = Persona(
                id_persona=data['id_persona'],
                primer_nombre=data['primer_nombre'],
                segundo_nombre=data.get('segundo_nombre'),
                apellidos=data['apellidos'],
                fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date(),
                genero=data['genero'],
                correo=data['correo'],
                celular=data['celular'],
                tipo_documento=data['tipo_documento'],
                foto=data.get('foto')
            )

            # Guardar en la base de datos
            db.session.add(nueva_persona)
            db.session.flush()  # Para obtener el ID generado

            # Registrar en el log
            log = Log(
                accion='crear',
                id_persona=nueva_persona.id_persona
            )
            db.session.add(log)

            # Confirmar transacción
            db.session.commit()

            return {
                'message': 'Persona registrada exitosamente',
                'persona': nueva_persona.to_dict()
            }

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al registrar persona: {str(e)}")

    @staticmethod
    def obtener_persona(id_persona):
        persona = Persona.query.get(id_persona)
        if persona:
            return persona.to_dict()
        return None

    @staticmethod
    def listar_personas():
        personas = Persona.query.all()
        return [persona.to_dict() for persona in personas]
