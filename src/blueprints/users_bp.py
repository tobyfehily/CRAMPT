from flask import Blueprint, request
from models.user import User, UserSchema
from setup import db


users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
def get_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=['password']).dump(users), 200

@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=['password']).dump(user), 200
    else:
        return {'error': 'User not found'}, 404
    
@users_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_user(id):
    user_info = UserSchema().load(request.json)
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        user.email = user_info.get('email', user.email)
        user.password = user_info.get('password', user.password)
        db.session.commit()
        return UserSchema().dump(user)
    else:
        return {'error': 'User not found'}, 404
    
@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'User not found'}, 404