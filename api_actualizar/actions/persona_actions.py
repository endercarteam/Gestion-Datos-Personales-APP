from models import db, Persona, Log
from datetime import datetime

class PersonaActions:
    @staticmethod
    def actualizar_persona(id_persona, data):
        persona = Persona.query.get(id_persona)
        if not persona:
            return None

        for key, value in data.items():
            if hasattr(persona, key):
                setattr(persona, key, value)

        db.session.add(persona)
        db.session.add(Log(accion='actualizar', id_persona=id_persona))
        db.session.commit()

        return persona.to_dict()

