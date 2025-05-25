from models import db, Log, Persona
from sqlalchemy import and_
from sqlalchemy import extract

class LogActions:
    @staticmethod
    def listar_logs():
        return [l.to_dict() for l in Log.query.all()]

    @staticmethod
    def buscar_logs(filtros):
        query = db.session.query(Log).join(Persona, Log.id_persona == Persona.id_persona)

        if 'tipo_documento' in filtros and filtros['tipo_documento']:
            query = query.filter(Persona.tipo_documento == filtros['tipo_documento'])

        if 'nro_documento' in filtros and filtros['nro_documento']:
            query = query.filter(Persona.nro_documento == filtros['nro_documento'])

        if 'fecha' in filtros and filtros['fecha']:
            fecha = filtros['fecha']
            try:
                partes = fecha.split("-")
                if len(partes) == 1:  # Solo año
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
                else:
                    raise ValueError("Formato de fecha no válido. Usa: YYYY o YYYY-MM o YYYY-MM-DD")
            except ValueError:
                raise ValueError("Formato de fecha incorrecto. Usa: YYYY o YYYY-MM o YYYY-MM-DD")
        if 'accion' in filtros and filtros['accion']:
            query = query.filter(Log.accion == filtros['accion'])
        logs = query.all()
        return [log.to_dict() for log in logs]
