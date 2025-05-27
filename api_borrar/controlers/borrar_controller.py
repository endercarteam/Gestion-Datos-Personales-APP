from actions.persona_actions import PersonaActions
from flask import jsonify

class PersonaController:
    @staticmethod
    def eliminar_persona(id_persona):
        try:
            return PersonaActions.borrar_persona_db(id_persona)
        except Exception as e:
            return jsonify({'error': f'Error interno: {str(e)}'}), 500
