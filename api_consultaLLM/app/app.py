
from flask import Flask, request, jsonfy 
from flask_sqlalchemy 
import SQLAlchemy 
from app.models import db 
import os
from app.routes import api

def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin123@db:5432/gestion_datos_personales'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	 db.init_app(app)    
    	# Registrar blueprints
    	app.register_blueprint(api, url_prefix='/api') 
	gemini_service =  GeminiService()

