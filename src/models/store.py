from setup import db, ma
from marshmallow import fields
from marshmallow.validate import Length


class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    suburb = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone_number = db.Column(db.String)

class StoreSchema(ma.Schema):
    email = fields.Email(required=True)

    class Meta:
        fields = ('id', 'name', 'address', 'suburb', 'state', 'email', 'phone number')