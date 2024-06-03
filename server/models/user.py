from config import db
from sqlalchemy_serializer import SerializerMixin


class User(db.Model,SerializerMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    profile_picture = db.Column(db.String(255),default='')
    role = db.Column(db.String(),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    

    