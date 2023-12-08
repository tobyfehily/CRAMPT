from flask import Blueprint
from setup import db, bcrypt
from models.user import User
from models.store import Store
from models.reports import Report

# Links the db_commands variable route with 
db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def db_create():
    # Drops all crampt tables
    db.drop_all()
    # Creates all crampt tables
    db.create_all()
    print('Created tables')


@db_commands.cli.command('seed')
def db_seed():
    # Creates multiple SQLAlchemy User instances
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
    # Inserts Users instances into the users table, with SQLAlchemy User model 
    # translating between Python class variables and SQL values
    db.session.add_all(users)
    # Commits changes to the database
    db.session.commit()
    
    # Creates multiple SQLAlchemy Store instances
    stores = [
            Store(
                name = "Chemist Warehouse Newmarket",
                address = "Shop 3 & 6 388 to 390 Racecourse Road",
                suburb = "Flemington",
                state = "Victoria",
                email = "newmarket@chemistwarehouse.com.au",
                phone_number = "0393767228",
                aisle_width = 53
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
                aisle_width = 51
            )
    ]
    # Inserts Store instances into the stores table, with SQLAlchemy Store model
    # translating between Python class variables and SQL values
    db.session.add_all(stores)
    # Commits changes to the database
    db.session.commit()

    # Creates multiple SQLAlchemy Report instances
    reports = [
        Report(
            user_id = users[0].id,
            store_id = users[0].id,
            aisle_width = 42
        ),
        Report(
            user_id = users[1].id,
            store_id = users[1].id,
            aisle_width = 43,
            image = "http://www.placekitten.com/100"
        ),
        Report(
            user_id = users[1].id,
            store_id = users[0].id,
            aisle_width = 44,
            image = "http://www.placekitten.com/100"
        )
    ]
    # Inserts Report instances into the reports table, with SQLAlchemy Report 
    # model translating between Python class variables and SQL values
    db.session.add_all(reports)
    # Commits changes to the database
    db.session.commit()

    print('Database seeded.')