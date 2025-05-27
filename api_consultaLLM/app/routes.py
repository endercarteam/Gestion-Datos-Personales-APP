from flask import Blueprint, request, jsonify
from app.controller import LLMControler 

api = Blueprint('api', __name__)

@api.route('/usuarios/llm', methods=['POST'])
def querry_llm():
	
	data = request.json
	if not data or 'querry' not in data:
		return jsonfy({"error": "Se requiere una consulta"}), 400

	try:
		response = controller.process_query(data['query'])
		return jsonify({"response": response})

	except Exception  as e:
		return jsonify({"error": f'Error interno: { str(e)}'}), 500
