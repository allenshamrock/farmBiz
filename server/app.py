from config import app,api,db
from models import User,Animal,Order,Transaction,Produce,uuid
from flask import request, jsonify, make_response,url_for,session
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, jwt_required, create_refresh_token
from datetime import datetime, timedelta
import os
import cloudinary
from cloudinary import uploader
import cloudinary.api
import jwt
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token

load_dotenv()


jwt_secret_key = os.getenv('JWT_SECRET_KEY')

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    api_base_uri="https://www.googleapis.com/oauth2/v1",
    client_kwargs={'scope': 'openid profile email'}
)

cloudinary.config(
    cloud_name = os.getenv('CLOUD_NAME'),
    api_key = os.getenv('API_KEY'),
    api_secret = os.getenv('API_SECRET')
)

app.config['SEND_API_KEY'] = os.getenv('SEND_API_KEY')
if not all([cloudinary.config().cloud_name, cloudinary.config().api_key, cloudinary.config().api_secret]):
    raise ValueError(
        "No Cloudinary configuration found. Ensure CLOUD_NAME, API_KEY, and API_SECRET are set.")


@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorized', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/login/authorized')
def authorized():
    token = google.authorize_access_token()
    if not token:
        return jsonify({'message': 'Authorization failed.'}), 400

    user_info = google.parse_id_token(token)
    email = user_info['email']
    username = user_info['name']

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(
        identity={"email": user.email, "role": user.role, "id": user.id})
    refresh_token = create_refresh_token(
        identity={"email": user.email, "role": user.role, "id": user.id})

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    })


class Signup(Resource):
    def post(self):
        app.logger.info(f"Form data: {request.form}")
        app.logger.info(f"Files: {request.files}")
        data = request.form

        file_to_upload = request.files.get('file')
        if not file_to_upload or file_to_upload.filename == '':
            return jsonify({"error": "File is required"}), 400

        try:
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            role = data.get("role")
            profile_url = data.get("profile")
            app.logger.info(
                f"Received Data: username:{username}, email:{email}, profile_url:{profile_url}, role:{role}"
            )

            # Validate missing fields
            missing_fields = [field for field in [
                "username", "email", "password", "profile"] if not data.get(field)]
            if missing_fields:
                return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

            # Upload file to Cloudinary
            try:
                if profile_url == 'image':
                    timestamp = str(int(datetime.utcnow().timestamp()))
                    upload_result = cloudinary.uploader.upload(
                        file_to_upload, resource_type='image',timestamp=timestamp)
                else:
                    return jsonify({"error": "Profile must be an image"}), 400
            except Exception as e:
                app.logger.error(f"Error uploading file to Cloudinary: {e}")
                return jsonify({"error": "File upload failed"}), 500

            file_url = upload_result.get('url')
            new_user = User(
                username=username,
                email=email,
                password=password,
                role=role,
                profile_picture=file_url,
                joined_at=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": f"{role} account created successfully"}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Username or email already exists"}), 400

        except Exception as e:
            app.logger.error(f"Unexpected error: {e}")
            return jsonify({"error": str(e)}), 500

class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({"error": "Invalid JSON payload"}), 400)

            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return make_response(jsonify({"error": "Email and password are required"}), 400)

            user = User.query.filter_by(email=email).first()
            if not user or not user.check_password(password):
                return make_response(jsonify({'error': 'Invalid email or password'}), 401)

            access_token = create_access_token(identity=str(user.id))

            response_data = {
                "message": "User logged in successfully",
                "token": access_token,
                "userId": str(user.id)
            }
            return make_response(jsonify(response_data), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


class Logout(Resource):
    def post(self):
        response = make_response(jsonify({'message': 'Logged out'}))
        response.delete_cookie('token')
        return response
class AnimalsRoutes(Resource):
    def get(self):
        animals = [animal.to_dict() for animal in Animal.query.all()]
        response = make_response(jsonify(animals), 200)
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

    def put(self, id):
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

    def delete(self, id):
        try:
            animal_uuid = uuid.UUID(id)  # Convert the string id to a UUID
        except ValueError:
            return make_response(jsonify({'message': "Invalid UUID format"}), 400)
        animal = Animal.query.get(animal_uuid)
        if animal:
            db.session.delete(animal)
            db.session.commit()
            response = make_response(
                jsonify({'message': 'Animal deleted successfully'}), 200)
            return response
        else:
            response = make_response(
                jsonify({'message': 'Animal not found'}), 404)
            return response


class OrderRoutes(Resource):
    def get(self):
        orders = Order.query.all()
        if not orders:
            response = make_response(
                jsonify({"message": "No orders found"}), 404)
            return response
        orders_dict = [order.to_dict() for order in orders]

        response = make_response(jsonify(orders_dict), 200)
        return response

    def post(self):
        data = request.json

        user_id = data.get('user_id')
        animal_id = data.get('animal_id')

        if not user_id or not animal_id:
            return make_response(jsonify({"message": "Both user_id and animal_id are required"}), 404)

        user = User.query.get(user_id)
        animal = Animal.query.get(animal_id)

        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        if not animal:
            return make_response(jsonify({"message": "Animal not found"}), 404)

        new_order = Order(
            user_id=user_id,
            animal_id=animal_id,
            status=data.get('status', 'pending')
        )
        db.session.add(new_order)
        db.session.commit()

        response = make_response(
            jsonify({"message": "Order created successfully"}), 201)
        return response


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
            farmer_id=uuid.UUID(data['farmer_id']),
            produce_type=data['produce_type'],
            quantity=data['quantity'],
            price=data['price']
        )

        db.session.add(new_produce)
        db.session.commit()
        return {"message": "Produce added successfully"}, 201


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



api.add_resource(Signup,'/signup')
api.add_resource(Login,'/login')
api.add_resource(Logout,'/logout')
api.add_resource(Transactions,'/transactions')
api.add_resource(AnimalsRoutes, '/animals', '/animals/<string:id>')
api.add_resource(OrderRoutes, '/orders')
api.add_resource(Produces, '/produces', '/produces/<string:id>')

if __name__ == '__main__':
    app.run(port=5555,debug=True)