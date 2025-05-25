# Gestion-Datos-Personales-APP
Aplicacion para la gestion de datos personales
# Distribucion de contenedores
/menu


/ui_registrar


/api_registrar


/ui_actualizar


/api_actualizar


/ui_borrar


/api_borrar


/ui_consultaLog


/api_consultaLog


/ui_consultaUsuarios


/api_consultaUsuarios


/ui_consultaLLM


/api_consultaLLM


/db


api routes:

- api_actualizar:
  
  @api.route('/usuarios/<int:id_persona>', methods=['PUT'])
  
- api_borrar
  
  @api.route('/eliminar/<int:id_persona>', methods=['DELETE'])
  
- api_consultausuarios:
  
  @api.route('/usuarios', methods=['GET'])
  
- api_registrar:
  
  @api.route('/usuarios', methods=['POST'])

- api_consultalogs:
  
  - listar todos los logs:
    
    @api.route('/logs', methods=['GET'])
  
  - buscar por filtros (id, fecha, accion, tipo de documento):
    
    @api.route('/logs/buscar', methods=['GET'])
