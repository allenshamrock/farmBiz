from models import Order,User,Animal
from flask import request, jsonify, make_response
from flask_restful import Resource
from config import db
class OrderRoutes(Resource):
    def get(self):
        orders = Order.query.all()
        if not orders:
            response = make_response(jsonify({"message":"No orders found"}),404)
            return response
        orders_dict = [order.to_dict() for order in orders]

        response = make_response(jsonify(orders_dict),200)
        return response
    
    def post(self):
        data = request.json

        user_id = data.get('user_id')
        animal_id = data.get('animal_id')

        if not user_id or not animal_id:
            return make_response(jsonify({"message":"Both user_id and animal_id are required"}),404)
        
        user = User.query.get(user_id)
        animal = Animal.query.get(animal_id)

        if not user:
            return make_response(jsonify({"message":"User not found"}),404)
        if not animal:
            return make_response(jsonify({"message":"Animal not found"}),404)
        
        new_order =Order(
            user_id = user_id,
            animal_id = animal_id,
            status=data.get('status','pending')
        )
        db.session.add(new_order)
        db.session.commit()

        response = make_response(jsonify({"message":"Order created successfully"}),201)
        return response
    