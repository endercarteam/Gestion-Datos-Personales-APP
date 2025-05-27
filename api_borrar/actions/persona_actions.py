from models import db, Persona, Log

class PersonaActions:
  def borrar_persona_db(id_persona):
      persona = Persona.query.get(id_persona)
    
      if not persona:
          return {'error': f'Persona con ID {id_persona} no encontrada.'}

    # Copiar el ID al log antes de eliminar
      log = Log(
          accion='eliminar',
          id_persona=id_persona  # ← Simple copia, no FK
      )
      db.session.add(log)

      db.session.delete(persona)
      db.session.commit()

      return {'mensaje': f'Persona con ID {id_persona} eliminada correctamente.'}

