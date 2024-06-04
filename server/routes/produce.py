from  flask_restful import Resource
from flask import make_response,jsonify,request 
from models import Produce, uuid
from config import db


class Produces(Resource):
    def get(self):
        produces = Produce.query.all()
        produce_list = []
        for produce in produces:
            produce_data = {
                'id': produce.id,
                'farmer_id': produce.farmer_id,
                'produce_type': produce.produce_type,
                'quantity': produce.quantity,
                'price': produce.price
            }
            produce_list.append(produce_data)

        response = make_response(jsonify(produce_list), 200)
        return response
    
    def post(self):
        data = request.json

        new_produce = Produce(
            farmer_id = uuid.UUID(data['farmer_id']),
            produce_type= data['produce_type'],
            quantity = data['quantity'],
            price = data['price']
        )
        
        db.session.add(new_produce)
        db.session.commit()
        return {"message":"Produce added successfully"}, 201
    

        