from flask_jwt_extended import get_jwt_identity
from models.user import User
from flask import abort
from setup import db


def authorise(user_id=None):
    # Retrieves id from JWT payload sub
    jwt_user_id = get_jwt_identity()
    # Selects from users table where the id from the JWT payload sub equals the
    # id of a user table tuple using SQLAlchemy User model
    stmt = db.select(User).filter_by(id=jwt_user_id)
    # Returns a ScalarResult object with the first value of the first result row
    user = db.session.scalar(stmt)
    # Triggers if matching tuple's is_admin attribute is False, or no matches
    # are found and the id from the JWT paylod sub does not equal the id of
    # the user table tuple
    if not (user.is_admin or (user_id and jwt_user_id == user_id)):
        abort(401)