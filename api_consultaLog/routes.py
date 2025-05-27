from flask import Blueprint, request, jsonify
from controlers.log_controller import LogController

api = Blueprint('api_consultalogs', __name__)

@api.route('/logs', methods=['GET'])
def listar_logs():
    return LogController.listar_logs()

@api.route('/logs/buscar', methods=['GET'])
def buscar_logs():
    try:
        filtros = {
            'id_persona': request.args.get('id_persona'),
            'tipo_documento': request.args.get('tipo_documento'),
            'fecha': request.args.get('fecha'),
            'accion': request.args.get('accion')
        }
        resultado = LogController.buscar_logs(filtros)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
