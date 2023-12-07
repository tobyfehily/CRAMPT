from flask import Blueprint
from setup import db, bcrypt
from models.user import User
from models.store import Store
from models.reports import Report

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def db_create():
    db.drop_all()
    db.create_all()
    print('Created tables')


@db_commands.cli.command('seed')
def db_seed():
    users = [
            User(
                email = 'admin@crampt.com',
                password=bcrypt.generate_password_hash('averysecurepassword').decode('utf8'),
                is_admin = True,
            ),
            User(
                email = 'samgance@chemistwarehouse.com.au',
                password=bcrypt.generate_password_hash('anotherverysecurepassword').decode('utf8'),
            )
    ]
    db.session.add_all(users)
    db.session.commit()
    
    stores = [
            Store(
                name = "Chemist Warehouse Newmarket",
                address = "Shop 3 & 6 388 to 390 Racecourse Road",
                suburb = "Flemington",
                state = "Victoria",
                email = "newmarket@chemistwarehouse.com.au",
                phone_number = "0393767228",
                aisle_width = 559
            ),
            Store(
                name = "Chemist Warehouse Ascot Vale",
                address = "Tenancy 1 568 to 570 Mount Alexander Road",
                suburb = "Ascot Vale",
                state = "Victoria",
                email = "ascotvale@chemistwarehouse.com.au",
                phone_number = "0393262388"
            ),
            Store(
                name = "Chemist Warehouse Sydney Pitt St",
                address = "1 249 to 251 Pitt Street",
                suburb = "Sydney",
                state = "New South Wales",
                email = "newmarket@chemistwarehouse.com.au",
                phone_number = "0292612305",
                aisle_width = 600
            )
    ]
    db.session.add_all(stores)
    db.session.commit()

    reports = [
        Report(
            user_id = users[0].id,
            store_id = users[0].id,
            aisle_width = 677
        ),
        Report(
            user_id = users[1].id,
            store_id = users[1].id,
            aisle_width = 677,
            image = "placekitten.com/200"
        ),
        Report(
            user_id = users[1].id,
            store_id = users[0].id,
            aisle_width = 678,
            image = "placekitten.com/300"
        )
    ]
    db.session.add_all(reports)
    db.session.commit()

    print('Database seeded.')