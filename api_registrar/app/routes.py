from flask import Blueprint, request, jsonify
from app.models import Person
from app import db

api = Blueprint('api', __name__)

@api.route('/add_person', methods=['POST'])
def add_person():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    if not name or not isinstance(age, int):
        return jsonify({'error': 'Invalid input'}), 400

    person = Person(name=name, age=age)
    db.session.add(person)
    db.session.commit()

    return jsonify({'message': f'Person {name} added.'}), 201
