from config import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    serialize_only = ('id', 'username', 'email', 'profile_picture', 'joined_at', 'role')
    serialize_exclude = ('password_hash',)

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    profile_picture = db.Column(db.String(255), default="")
    password_hash = db.Column(db.String(100), nullable=False)
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    role = db.Column(db.String(), nullable=False, default='user')

    transactions = db.relationship('Transaction', back_populates='user', cascade="all, delete-orphan")
    orders = db.relationship('Order', back_populates='user', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User id={self.id}, username={self.username}, role={self.role}>"

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": role,
    }


class Farmer(User):
    __mapper_args__ = {
        "polymorphic_identity": "farmer",
    }

    animals = db.relationship("Animal", back_populates="farmer", cascade="all, delete-orphan")


class Animal(db.Model, SerializerMixin):
    __tablename__ = "animals"
    serialize_only = ('id', 'type', 'breed', 'age', 'price', 'quantity', 'description','farmer')
    
    
    
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    farmer_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    type = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(250), nullable=False)

    farmer = db.relationship("Farmer", back_populates="animals")
    orders = db.relationship('Order', back_populates='animal', cascade="all, delete-orphan")    


class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"
    serialize_only = ('id','status','animal')

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    animal_id = db.Column(UUID(as_uuid=True), db.ForeignKey("animals.id"))
    status = db.Column(db.String(10), default='pending')

    user = db.relationship("User", back_populates="orders")
    animal = db.relationship("Animal", back_populates="orders")
    transaction = db.relationship("Transaction", back_populates='order', uselist=False)


class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'
    serialize_only = ('id', 'amount', 'quantity','order')    

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    amount = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))    
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey("orders.id"))

    user = db.relationship("User", back_populates="transactions")    
    order = db.relationship('Order', back_populates='transaction')

from sqlalchemy.orm import relationship

class User(db.Model,SerializerMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    profile_picture = db.Column(db.String(255),default='')
    password = db.Column(db.String())
    
class Animal(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("farmer.id"))
    type = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(250), nullable=False)

    farmer = db.relationship("Farmer", back_populates="animals " , cascade = 'all,delete-orphan')
    order = db.relationship(
        'Order', back_populates="animals", cascade='all,delete-orphan')
    transactions = db.relationship('Transaction', back_populates='animals')


class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"
    serialize_only = ('id','status','animal')

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    animal_id = db.Column(UUID(as_uuid=True), db.ForeignKey("animals.id"))
    status = db.Column(db.String(10), default='pending')

    user = db.relationship("User", back_populates="orders")
    animal = db.relationship("Animal", back_populates="orders")
    transaction = db.relationship("Transaction", back_populates='order', uselist=False)


class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'
    serialize_only = ('id', 'amount', 'quantity','order')    

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    amount = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))    
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey("orders.id"))

    user = db.relationship("User", back_populates="transactions")    
    order = db.relationship('Order', back_populates='transaction')
