from flask import Blueprint, request, jsonify
from app.controller import LLMController

api = Blueprint('api', __name__)
controller = LLMController()

@api.route('/usuarios/llm', methods=['POST'])
def query_llm():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Se requiere una consulta"}), 400

    try:
        response = controller.process_query(data['query'])
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": f'Error interno: {str(e)}'}), 500
