from flask import Blueprint, jsonify
from controlers.borrar_controller import PersonaController

api = Blueprint('api_borrar', __name__)

@api.route('/persona/<int:id_persona>', methods=['DELETE'])
def borrar_persona(id_persona):
    try:
        result = PersonaController.eliminar_persona(id_persona)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500
