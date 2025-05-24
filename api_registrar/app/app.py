from flask import Flask
from app.routes import api
import os
from app import db
import sqlalchemy.exc
import time
load_dotenv()  

    app = Flask(__name__)
    # 2. Lee la URI desde la variable de entorno
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)
    app.register_blueprint(api)

    with app.app_context():
        for _ in range(10):
            try:
                db.create_all()
                break
            except sqlalchemy.exc.OperationalError:
                print("⏳ Esperando a que la base de datos esté lista…")
                time.sleep(1)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
