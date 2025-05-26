from actions.log_actions import LogActions
from flask import jsonify

class LogController:
    @staticmethod
    def listar_logs():
        try:
            logs = LogActions.listar_logs()
            return jsonify(logs), 200
        except Exception as e:
            return jsonify({'error': f'Error interno: {str(e)}'}), 500

    def buscar_logs(filtros):
        try:
          resultados = LogActions.buscar_logs(filtros)

          logs = []
          for log in resultados:
              logs.append({
                  "id_log": log.id_log,
                  "accion": log.accion,
                  "fecha": log.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                  "id_persona": log.id_persona
              })
          
          return logs
          
        except Exception as e:
          return jsonify({"error": f"Error al buscar logs: {str(e)}"}), 500
