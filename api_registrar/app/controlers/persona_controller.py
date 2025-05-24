from app.actions.persona_actions import PersonaActions
import re

class PersonaController:
    @staticmethod
    def registrar_persona(data):
        # Validar campos requeridos
        required_fields = ['primer_nombre', 'apellidos', 'fecha_nacimiento',
                          'genero', 'correo', 'celular', 'tipo_documento',
                          'nro_documento']

        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"El campo '{field}' es requerido")

        # Validar formato de correo
        email_pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        if not re.match(email_pattern, data['correo']):
            raise ValueError("El formato del correo electrónico es inválido")

        # Validar formato de celular (10 dígitos)
        if not re.match(r'^[0-9]{10}$', data['celular']):
            raise ValueError("El celular debe contener exactamente 10 dígitos")

        # Validar que los nombres no contengan solo números
        if re.match(r'^[0-9]+$', data['primer_nombre']):
            raise ValueError("El primer nombre no puede contener solo números")

        if 'segundo_nombre' in data and data['segundo_nombre'] and re.match(r'^[0-9]+$', data['segundo_nombre']):
            raise ValueError("El segundo nombre no puede contener solo números")

        if re.match(r'^[0-9]+$', data['apellidos']):
            raise ValueError("Los apellidos no pueden contener solo números")

        # Validar género
        valid_generos = ['Masculino', 'Femenino', 'No binario', 'Prefiero no reportar']
        if data['genero'] not in valid_generos:
            raise ValueError(f"El género debe ser uno de: {', '.join(valid_generos)}")

        # Validar tipo de documento
        valid_tipos_doc = ['Tarjeta de identidad', 'Cédula']
        if data['tipo_documento'] not in valid_tipos_doc:
            raise ValueError(f"El tipo de documento debe ser uno de: {', '.join(valid_tipos_doc)}")

        # Si todas las validaciones pasan, registrar la persona
        return PersonaActions.registrar_persona(data)

    @staticmethod
    def obtener_persona(id_persona):
        if not isinstance(id_persona, int) or id_persona <= 0:
            raise ValueError("El ID de persona debe ser un número entero positivo")

        return PersonaActions.obtener_persona(id_persona)

    @staticmethod
    def listar_personas():
        return PersonaActions.listar_personas()
