from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Persona(db.Model):
    __tablename__ = 'persona'
    id_persona = db.Column(db.Integer, primary_key=True)
    primer_nombre = db.Column(db.String(30), nullable=False)
    segundo_nombre = db.Column(db.String(30), nullable=True)
    apellidos = db.Column(db.String(60), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.Enum('Masculino', 'Femenino', 'No binario', 'Prefiero no reportar'), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(10), nullable=False)
    tipo_documento = db.Column(db.Enum('Tarjeta de identidad', 'Cédula'), nullable=False)
    foto = db.Column(db.String(255), nullable=True)


    def to_dict(self):
        return {
            'id_persona': self.id_persona,
            'primer_nombre': self.primer_nombre,
            'segundo_nombre': self.segundo_nombre,
            'apellidos': self.apellidos,
            'fecha_nacimiento': self.fecha_nacimiento.strftime('%Y-%m-%d'),
            'genero': self.genero,
            'correo': self.correo,
            'celular': self.celular,
            'tipo_documento': self.tipo_documento,
            'foto': self.foto
        }

class Log(db.Model):
    __tablename__ = 'log'

    id_log = db.Column(db.Integer, primary_key=True, autoincrement=True)
    accion = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    id_persona = db.Column(db.Integer,nullable=False)

    def to_dict(self):
        return {
            'id_log': self.id_log,
            'accion': self.accion,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'id_persona': self.id_persona
        }
