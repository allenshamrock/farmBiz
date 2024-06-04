from models import Animal,uuid
from flask import request, jsonify, make_response
from config import db
from flask_restful import Resource


class AnimalsRoutes(Resource):
    def get(self):
        animals=[animal.to_dict() for animal in Animal.query.all()]        
        response= make_response(jsonify(animals),200)
        return response
       
    def post(self):
        data = request.json

        new_animal = Animal(            
            farmer_id=uuid.UUID(data['farmer_id']),
            type=data['type'],
            breed=data['breed'],
            age=data['age'],
            price=data['price'],
            quantity=data['quantity'],
            description=data['description']
        )

        db.session.add(new_animal)
        db.session.commit()
        return {"message": "Animal added successfully"}, 201

    def put(self,id):
        try:
            animal_uuid = uuid.UUID(id)  # Convert the string id to a UUID 
        except ValueError:
            return make_response(jsonify({'message': "Invalid UUID format"}), 400)

        animal = Animal.query.get(animal_uuid)
        if animal:
            data = request.json
            animal.type = data.get('type', animal.type)
            animal.breed = data.get('breed', animal.breed)
            animal.age = data.get('age', animal.age)
            animal.price = data.get('price', animal.price)
            animal.quantity = data.get('quantity', animal.quantity)
            animal.description = data.get('description', animal.description)

            db.session.commit()

            response = make_response(
                jsonify({'message': "Animal updated successfully"}), 200)
            return response
        else:
            response = make_response(
                jsonify({'message': "Animal not found"}), 404)
            return response
    
    def delete(self,id):
        try:
            animal_uuid = uuid.UUID(id)  # Convert the string id to a UUID
        except ValueError:
            return make_response(jsonify({'message': "Invalid UUID format"}), 400)
        animal = Animal.query.get(animal_uuid)
        if animal:
            db.session.delete(animal)
            db.session.commit()
            response =  make_response(jsonify({'message':'Animal deleted successfully'}),200)
            return response
        else:
            response = make_response(jsonify({'message':'Animal not found'}),404)
            return response
