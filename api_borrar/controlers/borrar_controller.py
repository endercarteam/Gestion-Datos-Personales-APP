from actions.persona_actions import PersonaActions
from flask import jsonify

class PersonaController:
    @staticmethod
    def borrar_persona(id_persona):
        try:
            success = PersonaActions.borrar_persona(id_persona)
            if success:
                return jsonify({'message': 'Persona eliminada correctamente'}), 200
            return jsonify({'error': 'Persona no encontrada'}), 404
        except Exception as e:
            return jsonify({'error': f'Error interno: {str(e)}'}), 500
