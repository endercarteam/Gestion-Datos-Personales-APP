from actions.persona_actions import ConsultaActions,UsuarioActions 
from flask import jsonify

class ConsultaController:
    @staticmethod
    def listar_usuarios():
        try:
            return ConsultaActions.listar_personas()
        except Exception as e:
            raise Exception(f"Error al listar personas: {str(e)}")
    def obtener_usuario(id_persona):
        try:
             return UsuarioActions.obtener_usuario(id_persona)
        except Exception as e:
            return jsonify({'error': f'Error al obtener usuario: {str(e)}'}), 500
