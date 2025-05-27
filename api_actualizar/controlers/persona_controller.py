from actions.persona_actions import PersonaActions
from flask import jsonify

class ActualizarController:
    @staticmethod
    def actualizar_persona(id_persona, data):
        try:
            return PersonaActions.actualizar_persona(id_persona, data)
        except Exception as e:
            return jsonify({'error': f'Error interno: {str(e)}'}), 500

