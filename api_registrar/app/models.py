
from app import db

class Person(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	age = db.Column(db.Integer)

