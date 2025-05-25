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
            return LogActions.buscar_logs(filtros)
        except ValueError as ve:
            raise ValueError(str(ve))
        except Exception as e:
            raise Exception(f"Error al buscar logs: {str(e)}")
