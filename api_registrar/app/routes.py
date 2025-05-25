from flask import Blueprint, request, jsonify
from .controlers.persona_controller import PersonaController

api = Blueprint('api', __name__)

@api.route('/persona', methods=['POST'])
def registrar_persona():
    try:
        data = request.get_json()
        result = PersonaController.registrar_persona(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@api.route('/persona/<int:id_persona>', methods=['GET'])
def obtener_persona(id_persona):
    try:
        result = PersonaController.obtener_persona(id_persona)
        if result:
            return jsonify(result), 200
        return jsonify({'error': 'Persona no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@api.route('/personas', methods=['GET'])
def listar_personas():
    try:
        result = PersonaController.listar_personas()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500
