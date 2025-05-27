from flask import Blueprint, request, jsonify
from controlers.persona_controller import ActualizarController

api = Blueprint('actualizar_api', __name__)

@api.route('/usuarios/<int:id_persona>', methods=['PUT'])
def actualizar_persona(id_persona):
    try:
        data = request.get_json()
        result = ActualizarController.actualizar_persona(id_persona, data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
