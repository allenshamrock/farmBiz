from models import User, Farmer, Animal, Order, Transaction, Produce
from config import app, db
from werkzeug.security import generate_password_hash
from faker import Faker
import random

fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    def generate_test_users(count=8):
        for _ in range(count):
            username = fake.user_name()
            user = User(
                username=username,
                email=f"{username}@gmail.com",
                profile_url=fake.image_url(),
                password_hash=generate_password_hash('password'),
            )
            db.session.add(user)
        db.session.commit()

    def generate_test_farmers(count=4):
        for _ in range(count):
            username = fake.user_name()
            user = Farmer(
                username=username,
                email=f'{username}@gmail.com',
                password_hash=generate_password_hash('password'),
                profile_url='https://cdn-icons-png.flaticon.com/512/3135/3135715.png',
                role='farmer'
            )
            db.session.add(user)
        db.session.commit()

    def generate_test_animals(count=4):
        farmers = Farmer.query.all()
        animal_types = ['cow', 'dog', 'cat']
        breeds = ['rotwiler', 'G-s', 'Rfeed']

        for _ in range(count):
            farmer = random.choice(farmers)
            animal_type = random.choice(animal_types)
            breed = random.choice(breeds)

            animal = Animal(
                farmer_id=farmer.id,
                type=animal_type,
                breed=breed,
                age=fake.random_int(min=2, max=5),
                price=fake.random_int(min=10000, max=500000),
                quantity=fake.random_int(min=1, max=50),
                description=fake.paragraph(),
            )
            db.session.add(animal)

        db.session.commit()

    def generate_test_orders(count=10):
        users = User.query.filter_by(role='user').all()
        animals = Animal.query.all()
        produces = Produce.query.all()
        states = ['pending', 'accepted', 'rejected']

        for _ in range(count):
            user = random.choice(users)
            animal = random.choice(animals)
            produce = random.choice(produces)
            state = random.choice(states)
            order = Order(
                user_id=user.id,
                animal_id=animal.id,
                produce_id=produce.id,
                status=state
            )
            db.session.add(order)
        db.session.commit()

    def generate_test_transactions(count=2):
        users = User.query.filter_by(role='user').all()
        orders = Order.query.filter_by(status='accepted').all()

        for _ in range(count):
            user = random.choice(users)
            order = random.choice(orders)
            transaction = Transaction(
                amount=fake.random_int(min=1000, max=500000),
                quantity=fake.random_int(min=1, max=50),
                user_id=user.id,
                order_id=order.id
            )
            db.session.add(transaction)
        db.session.commit()

    def generate_test_produces(count=4):
        farmers = Farmer.query.all()
        produce_types = ['peas', 'rice', 'beans', 'sorghum']

        for _ in range(count):
            farmer = random.choice(farmers)
            produce_type = random.choice(produce_types)

            produce = Produce(
                farmer_id=farmer.id,
                produce_type=produce_type,
                price=fake.random_int(min=10000, max=500000),
                quantity=fake.random_int(min=1, max=50),
            )
            db.session.add(produce)
        db.session.commit()

    generate_test_users()
    generate_test_farmers()
    generate_test_animals()
    generate_test_produces()
    generate_test_orders()
    generate_test_transactions()
