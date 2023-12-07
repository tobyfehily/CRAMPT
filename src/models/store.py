from setup import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length


class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    suburb = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone_number = db.Column(db.String)
    aisle_width = db.Column(db.Integer)

    reports = db.relationship('Report', back_populates='store', cascade="all, delete")

class StoreSchema(ma.Schema):
    reports = fields.Nested('ReportSchema', exclude=['store'], many=True)
    phone_number = fields.String(validate=And(
        Regexp('^[0-9]+$', error = "Phone number must contain only digits."),
        Length(equal=10, error = "Phone number must be 10 digits long.")
        )
    )
    # email = fields.Email(required=True)

    class Meta:
        fields = ('id', 'name', 'address', 'suburb', 'state', 'email', 'phone_number', 'reports', 'aisle_width')