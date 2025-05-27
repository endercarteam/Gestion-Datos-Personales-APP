from models import db, Persona, Log
from datetime import datetime

class ConsultaActions:
    @staticmethod
    def listar_personas():
        personas = Persona.query.all()
        log = Log(accion="consulta")
        db.session.add(log)
        db.session.commit()

        return [p.to_dict() for p in personas]
class UsuarioActions:
    @staticmethod
    def obtener_usuario(id_persona):
        try:
            persona = Persona.query.get(id_persona)
            if persona:
                log = Log(accion="consulta",id_persona=id_persona)
                db.session.add(log)
                db.session.commit()
                return persona.to_dict()
            return None
        except Exception as e:
            raise Exception(f"Error al obtener persona: {str(e)}")
