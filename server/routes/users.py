from flask_restful import Resource
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash,check_password_hash
from models import User
from sqlalchemy.exc import IntegrityError
from config import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime,timedelta
import os
import jwt
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token

load_dotenv()

jwt_secret_key = os.getenv('JWT_SECRET_KEY')
class Signup(Resource):
    def post(self):
        data = request.get_json()

        if data is None:
            return make_response(jsonify({"error": "Invalid JSON payload"}), 400)

        try:
            username = data["username"]
            email = data["email"]
            password = data["password"]
            role = data["role"]
            profile_url = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
            hashed_password = generate_password_hash(password, method="pbkdf2:sha512")

            user = User(
                username=username,
                email=email,
                password_hash=hashed_password,
                role=role,
                profile_picture=profile_url,
                joined_at=datetime.utcnow()
            )
            db.session.add(user)
            db.session.commit()

            return make_response(
                jsonify({"message": f"{role} account created successfully"}), 201
            )

        except IntegrityError:
            db.session.rollback()
            return make_response(
                jsonify({"error": "Username or email already exists"}), 400
            )

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


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

            # Generate JWT token
            access_token = create_access_token(identity=str(user.id))

            # Return response with token
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