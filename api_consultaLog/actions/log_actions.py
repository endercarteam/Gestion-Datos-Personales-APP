from models import db, Log, Persona
from sqlalchemy import and_
from sqlalchemy import extract
from sqlalchemy.orm import aliased

class LogActions:
    @staticmethod
    def listar_logs():
        return [l.to_dict() for l in Log.query.all()]

    @staticmethod
    def buscar_logs(filtros):
      db.session.expire_all()  # Asegura datos actualizados

      query = db.session.query(Log).outerjoin(Persona, Log.id_persona == Persona.id_persona)

      if 'tipo_documento' in filtros and filtros['tipo_documento']:
          query = query.filter(Persona.tipo_documento == filtros['tipo_documento'])

   
      if 'id_persona' in filtros and filtros['id_persona']:
          try:
              query = query.filter(Log.id_persona == int(filtros['id_persona']))
          except ValueError:
              pass  # ignorar si el valor no es un entero

    
      if 'accion' in filtros and filtros['accion']:
          query = query.filter(Log.accion.ilike(filtros['accion']))

    
      if 'fecha' in filtros and filtros['fecha']:
          try:
              partes = filtros['fecha'].split("-")
              if len(partes) == 1:  # Año
                  año = int(partes[0])
                  query = query.filter(extract('year', Log.fecha) == año)
              elif len(partes) == 2:  # Año y mes
                  año, mes = map(int, partes)
                  query = query.filter(
                      extract('year', Log.fecha) == año,
                      extract('month', Log.fecha) == mes
                  )
              elif len(partes) == 3:  # Año, mes y día
                  año, mes, dia = map(int, partes)
                  query = query.filter(
                      extract('year', Log.fecha) == año,
                      extract('month', Log.fecha) == mes,
                      extract('day', Log.fecha) == dia
                  )
          except Exception as e:
              print(f"Error procesando fecha: {e}")

      return query.order_by(Log.fecha.desc()).all()
