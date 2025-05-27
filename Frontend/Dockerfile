# Usa una imagen base de Nginx
FROM nginx:alpine

# Elimina la configuración por defecto de nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia tu configuración personalizada
COPY nginx.conf /etc/nginx/conf.d

# Copia todo el contenido del frontend al directorio donde nginx sirve archivos
COPY . /usr/share/nginx/html
