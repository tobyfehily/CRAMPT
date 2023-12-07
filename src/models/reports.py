from setup import db, ma
from marshmallow import fields
from marshmallow.validate import URL
from datetime import datetime


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)

    aisle_width = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String)
    date_created = db.Column(db.Date(), default = datetime.now().strftime("%Y-%m-%d"))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    user = db.relationship('User', back_populates='reports')
                           
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable = False)
    store = db.relationship('Store', back_populates='reports')


class ReportSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['id', 'email'])
    store = fields.Nested('StoreSchema', only=['id', 'name', 'aisle_width'])
    aisle_width = fields.Integer(strict=True)
    image = fields.String(validate=URL())

    class Meta:
        fields = ('id', 'aisle_width', 'image', 'date_created', 'user_id', 'store_id')