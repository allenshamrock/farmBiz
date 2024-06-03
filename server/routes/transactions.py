from flask_restful import Resource
from flask import make_response, jsonify, request
from models import Transaction, uuid, Order
from config import db


class Transactions(Resource):
    def get(self):
        transactions = [
            transaction.to_dict() for transaction in Transaction.query.all()
        ]
        response = make_response(jsonify(transactions), 200)
        return response

    def post(self):
        data = request.json
        price = data["amount"]
        orderId = uuid.UUID(data["orderId"])
        userId = uuid.UUID(data["userId"])
        quantity = data["quantity"]
        order = Order.query.get(orderId)

        if order:

            animal = order.animal
            if animal:
                if animal.price != price:
                    return {
                        "message": "amount entered is not the amount specified"
                    }, 417

                transaction = Transaction(
                    amount=price,
                    quantity=quantity,
                    user_id=userId,
                    order_id=orderId,
                )
                db.session.add(transaction)
                db.session.commit()

                new_quantity = animal.quantity - transaction.quantity
                animal.quantity = new_quantity
                db.session.commit()

        return {"message": "Transaction posted succesfully"}, 201
