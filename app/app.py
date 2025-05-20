from flask import Flask
from app.routes import api
from app import db
import sqlalchemy.exc
import time

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/mydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(api)

    with app.app_context():
        for _ in range(10):  # intentar durante ~10 segundos
            try:
                db.create_all()
                break
            except sqlalchemy.exc.OperationalError:
                print("⏳ Esperando a que la base de datos esté lista...")
                time.sleep(1)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)

