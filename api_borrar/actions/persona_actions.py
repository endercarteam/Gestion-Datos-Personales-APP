from models import db, Persona, Log

class PersonaActions:
  @staticmethod
  def eliminar_persona(id_persona):
      try:
          persona = Persona.query.get(id_persona)
          if not persona:
              return {'error': 'Persona no encontrada'}, 404

          persona.activo = False  # Soft delete
          db.session.commit()
  
          # Registrar en logs
          log = Log(
              accion='eliminar',
              id_persona=id_persona
          )
          db.session.add(log)
          db.session.commit()

          return {'message': 'Persona desactivada correctamente'}
      except Exception as e:
          db.session.rollback()
          raise Exception(f"Error al eliminar persona: {str(e)}")

