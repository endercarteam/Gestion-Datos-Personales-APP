FROM postgres:16

ENV POSTGRES_DB=gestion_datos_personales
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin123

COPY init.sql /docker-entrypoint-initdb.d/
