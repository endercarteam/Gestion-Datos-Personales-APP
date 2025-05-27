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
  
  http://localhost:5002/api/usuarios/id_persona
  Method: 'PUT'
  
- api_borrar
  
  http://localhost:5003/api/eliminar/id_persona
  
- api_consultausuarios:
  
  - listar todos los usuarios:
    
    http://localhost:5001/api/usuarios
  
  -buscar por id:

    http://localhost:5001/api/usuarios/id_persona
  
- api_registrar:
  
  http://localhost:5000/api/usuarios
  Method: 'Post'
- api_consultalogs:
  
  - listar todos los logs:
    
    http://localhost:5004/api/logs
  
  - buscar por filtros (id, fecha, accion, tipo de documento):
    
    http://localhost:5004/api/logs/buscar?filtro=valor&filtro=valor
