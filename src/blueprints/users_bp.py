from flask import Blueprint, request
from models.user import User, UserSchema
from setup import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta
from models.reports import Report, ReportSchema
from auth import authorise
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__, url_prefix='/users')

# Get all users
@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    authorise()
    # Selects all user tuples from user table using SQLAlchemy User model
    stmt = db.select(User)
    # Returns a ScalarResult object with the first value of each result row
    users = db.session.scalars(stmt).all()
    # Converts object into JSON using Marshmallow ReportSchema, excluding
    # password and reports, and dumps
    return UserSchema(many=True, exclude=['password', 'reports']).dump(users), 200

# Update a user
@users_bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
    # Loads JSON data and converts it to a Marshmallow UserSchema instance, 
    # excluding any id or is_admin values retrieved
    user_info = UserSchema(exclude=['id', 'is_admin']).load(request.json)
    # Selects from users table where the route id passed to the function
    # equals the id of a user table tuple using SQLAlchemy User model
    stmt = db.select(User).filter_by(id=user_id)
    # Returns a ScalarResult object with the first value of the first result row
    user = db.session.scalar(stmt)
    # Triggers if ScalarResult object retrieves a matching tuple from users 
    # table; otherwise, if no matches are found, skips
    if user:
        authorise(user.id)
        # Updates ScalarResult object email with email from Marshmallow 
        # UserSchema instance, otherwise defaulting to existing ScalarResult 
        # object email        
        user.email = user_info.get('email', user.email)
        # Updates ScalarResult object password with password from Marshmallow 
        # UserSchema instance, otherwise defaulting to existing ScalarResult 
        # object password        
        user.password = user_info.get('password', user.password)
        # Commits changes to the database
        db.session.commit()
        # Converts User instance into JSON using Marshmallow UserSchema,
        # excluding id and is_admin values, and dumps 
        return UserSchema(exclude=['id', 'is_admin', 'reports']).dump(user)
    else:
        return {'error': 'User not found'}, 404

# Delete a user   
@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # Selects from users table where the route id passed to the function
    # equals the id of a user table tuple using SQLAlchemy User model
    stmt = db.select(User).filter_by(id=user_id)
    # Returns a ScalarResult object with the first value of the first result row
    user = db.session.scalar(stmt)
    # Triggers if ScalarResult object retrieves a matching tuple from users 
    # table; otherwise, if no matches are found, skips
    if user:
        authorise(user.id)
        # Deletes tuple from reports table
        db.session.delete(user)
        # Commits changes to database
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'User not found'}, 404
    
# Get a user's reports
@users_bp.route('<int:user_id>/reports', methods=['GET'])
@jwt_required()
def get_user_reports(user_id):
    authorise(user_id)
    # Selects from reports table where the route id passed to the function
    # equals the user_id of a report table tuple using SQLAlchemy Report model
    stmt = db.select(Report).filter_by(user_id=user_id)
    # Returns a ScalarResult object with the first value of each result row
    reports = db.session.scalars(stmt).all()
    # Converts object into JSON using Marshmallow ReportSchema, excluding
    # user_id, and dumps
    return ReportSchema(many=True, exclude=['user_id']).dump(reports), 200

# Register as a user
@users_bp.route('/register', methods=['POST'])
def register():
    try:
        # Loads JSON data and converts it to a Marshmallow UserSchema 
        # instance, excluding any id or is_admin values retrieved
        user_info = UserSchema(exclude=['id', 'is_admin']).load(request.json)
        # Creates a SQLAlchemy User instance, retrieving email, and retrieving 
        # then encrypting password, from the Marshmallow UserSchema instance        
        user = User(
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info["password"]).decode('utf8')
        )
        # Inserts User instance into the users table, with SQLAlchemy User 
        # model translating between Python class variables and SQL values
        db.session.add(user)
        # Commits changes to the database
        db.session.commit()
        # Converts User instance into JSON using Marshmallow UserSchema,
        # excluding password, reports and is_admin, and dumps
        return UserSchema(exclude=['password', 'reports', 'is_admin']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use.'}, 409

# Log in as a user 
@users_bp.route('/login', methods=['POST'])
def login():
    # Loads JSON data and converts it to a Marshmallow UserSchema 
    # instance, excluding any id or is_admin values retrieved
    user_info = UserSchema(exclude=['id', 'is_admin']).load(request.json)
    # Selects from users table where the email from the Marshmallow UserSchema
    # equals the email of a user table tuple using SQLAlchemy User model
    stmt = db.select(User).where(User.email==user_info["email"])
    # Returns a ScalarResult object with the first value of the first result row
    user = db.session.scalar(stmt)
    # Triggers if ScalarResult object retrieves a matching tuple from stores 
    # table and encrypted password from the Marshmallow UserSchema equals the 
    # encrypted password of the matching tuple; otherwise, if no matches 
    # are found or the encrypted passwords do not match, skips
    if user and bcrypt.check_password_hash(user.password, user_info["password"]):
        # Generates a JSON token, where the payload sub is the matching tuple's
        # id, which will expire in one day
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        # Converts User instance into JSON using Marshmallow UserSchema,
        # including only email and id, and dumps, with JSON token.
        return {'token': token, 'user': UserSchema(only=['email', 'id']).dump(user)}
    else:
        return {"error": "Invalid email or password."}, 409   