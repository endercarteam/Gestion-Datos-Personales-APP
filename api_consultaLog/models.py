from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Persona(db.Model):
    __tablename__ = 'persona'
    id_persona = db.Column(db.Integer, primary_key=True)
    primer_nombre = db.Column(db.String(30), nullable=False)
    segundo_nombre = db.Column(db.String(30))
    apellidos = db.Column(db.String(60), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    genero = db.Column(db.Enum('Masculino', 'Femenino', 'No binario', 'Prefiero no reportar'))
    correo = db.Column(db.String(100))
    celular = db.Column(db.String(10))
    tipo_documento = db.Column(db.Enum('Tarjeta de identidad', 'Cédula'))
    nro_documento = db.Column(db.String(10))
    foto = db.Column(db.String(255))

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Log(db.Model):
    __tablename__ = 'log'

    id_log = db.Column(db.Integer, primary_key=True)
    accion = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id_persona'), nullable=True)

    def to_dict(self):
        return {
            'id_log': self.id_log,
            'accion': self.accion,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'id_persona': self.id_persona
        }

