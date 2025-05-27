from flask import Blueprint, request, jsonify
from controlers.persona_controller import ConsultaController

api = Blueprint('api_consulta_usuarios', __name__)

@api.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        result = ConsultaController.listar_usuarios()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f"Error al listar personas: {str(e)}"}), 500

@api.route('/usuarios/<int:id_persona>', methods=['GET'])
def obtener_usuario(id_persona):
    try:
        result = ConsultaController.obtener_usuario(id_persona)
        if result:
            return jsonify(result), 200
        return jsonify({'error': 'Persona no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': f"Error al obtener persona: {str(e)}"}), 500

