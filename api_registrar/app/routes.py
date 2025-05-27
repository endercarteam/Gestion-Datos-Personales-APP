from flask import Blueprint, request, jsonify
from .controlers.persona_controller import PersonaController

api = Blueprint('api', __name__)

@api.route('/usuarios', methods=['POST'])
def registrar_persona():
    try:
        data = request.get_json()
        result = PersonaController.registrar_persona(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500
