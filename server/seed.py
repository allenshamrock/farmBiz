from models import User,Animal,Order,Transaction
from config import app,db
from werkzeug.security import generate_password_hash
from faker import Faker
from sqlalchemy.exc import IntegrityError
import random

fake = Faker()

with app.app_context():
    # User.query.delete()
    # Animal.query.delete()
    # Order.query.delete()
    # Transaction.query.delete()
    db.drop_all()
    db.create_all()

    def generate_test_users(count=8):
        for _ in range(count):
            username = fake.user_name()                 
            user = User(
                username = username,
                email = f"{username}@gmail.com",
                profile_picture = fake.image_url(),
                password_hash=generate_password_hash('password'),                              
            )
            db.session.add(user)
        db.session.commit()
        # Import necessary modules and models

    def generate_test_famers(count=4):
        # Create an admin user
        for _ in range(count):
            username = fake.user_name()
            
            user = User(
                username=username,
                email=f'{username}@gmail.com',
                password_hash=generate_password_hash('password'),
                profile_picture ='https://cdn-icons-png.flaticon.com/512/3135/3135715.png',  
                role ='farmer'  
            )
            db.session.add(user)
        db.session.commit()                    

    def generate_test_animals(count=4):
        users = User.query.filter_by(role='farmer').all()
        animal_types = ['cow', 'dog', 'cat']  # Corrected animal types list
        breeds = ['rotwiler', 'G-s', 'Rfeed']  # Corrected breeds list

        for _ in range(count):
            farmer = random.choice(users)
            animal_type = random.choice(animal_types)  # Select a random animal type
            breed = random.choice(breeds)  # Select a random breed

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
        states = ['pending','accepted','rejected']
        for _ in range(count):
            user =random.choice(users)
            animal =random.choice(animals)
            state = random.choice(states)
            order = Order(
                user_id = user.id,
                animal_id = animal.id,
                status = state
            )
            db.session.add(order)
        db.session.commit()

    def generate_test_transaction(count=2):        
        users = User.query.filter_by(role='user').all()
        orders = Order.query.filter_by(status='accepted').all()

        for _ in range(count):
            user =random.choice(users)                       
            order =random.choice(orders)      
            transaction = Transaction(
                amount = fake.random_int(min=1000,max=500000),
                quantity = fake.random_int(min=1,max=50),
                user_id = user.id,                
                order_id = order.id
            )
            db.session.add(transaction)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        generate_test_users()
        generate_test_famers()
        generate_test_animals()
        generate_test_orders()
        generate_test_transaction()
