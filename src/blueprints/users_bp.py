from flask import Blueprint, request
from models.user import User, UserSchema
from setup import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta
from models.reports import Report, ReportSchema

users_bp = Blueprint('users', __name__, url_prefix='/users')

# Get all users
@users_bp.route('/', methods=['GET'])
def get_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=['password', 'reports']).dump(users), 200

# Get a user
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=['password']).dump(user), 200
    else:
        return {'error': 'User not found'}, 404

# Update a user
@users_bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    user_info = UserSchema(exclude=['id', 'is_admin']).load(request.json)
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        user.email = user_info.get('email', user.email)
        user.password = user_info.get('password', user.password)
        db.session.commit()
        return UserSchema(exclude=['id', 'is_admin', 'reports']).dump(user)
    else:
        return {'error': 'User not found'}, 404

# Delete a user   
@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'User not found'}, 404
    
# Get a user's reports
@users_bp.route('<int:user_id>/reports', methods=['GET'])
def get_user_reports(user_id):
    stmt = db.select(Report).filter_by(user_id=user_id)
    reports = db.session.scalars(stmt).all()
    return ReportSchema(many=True, exclude=['user']).dump(reports), 200

# Register as a user
@users_bp.route('/register', methods=['POST'])
def register():
    try:
        user_info = UserSchema(exclude=['id', 'is_admin']).load(request.json)
        
        user = User(
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info["password"]).decode('utf8')
        )

        db.session.add(user)
        db.session.commit()

        return UserSchema(exclude=['password', 'reports', 'is_admin']).dump(user), 201
    
    except IntegrityError:
        return {'error': 'Email address already in use.'}, 409

# Log in as a user 
@users_bp.route('/login', methods=['POST'])
def login():
    user_info = UserSchema().load(request.json)

    stmt = db.select(User).where(User.email==user_info["email"])
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, user_info["password"]):
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=7))
        return {'token': token, 'user': UserSchema(only=['email', 'id']).dump(user)}
    else:
        return {"error": "Invalid email or password."}, 409   