from flask import Blueprint, request
from models.store import Store, StoreSchema
from setup import db


stores_bp = Blueprint('stores', __name__, url_prefix='/stores')

@stores_bp.route('/', methods=['GET'])
def get_stores():
    stmt = db.select(Store)
    stores = db.session.scalars(stmt).all()
    return StoreSchema(exclude=['reports'], many=True).dump(stores), 200

@stores_bp.route('/<int:id>', methods=['GET'])
def get_store(id):
    stmt = db.select(Store).filter_by(id=id)
    store = db.session.scalar(stmt)
    if store:
        return StoreSchema(exclude=['reports']).dump(store), 200
    else:
        return {'error': 'Store not found'}, 404

@stores_bp.route('/', methods=['POST'])
def set_store():
    store_info = StoreSchema(exclude=['id']).load(request.json)
    store = Store(
        name = store_info['name'],
        address = store_info['address'],
        suburb = store_info['suburb'],
        state = store_info['state'],
        email = store_info.get('email', ''),
        phone_number = store_info.get('phone_number', None),
        aisle_width = store_info.get('aisle_width', None)
        )
    db.session.add(store)
    db.session.commit()
    return StoreSchema().dump(store), 201

@stores_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_store(id):
    store_info = StoreSchema().load(request.json)
    stmt = db.select(Store).filter_by(id=id)
    store = db.session.scalar(stmt)
    if store:
        store.name = store_info.get('name', store.name),
        store.address = store_info.get('address', store.address),
        store.suburb = store_info.get('suburb', store.suburb),
        store.state = store_info.get('state', store.state),
        store.email = store_info.get('email', store.email),
        store.phone_number = store_info.get('phone_number', store.phone_number),
        store.aisle_width = store_info.get('aisle_width', store.aisle_width)
        db.session.commit()
        return StoreSchema(exclude=['reports']).dump(store)
    else:
        return {'error': 'Store not found'}, 404
    
@stores_bp.route('/<int:id>', methods=['DELETE'])
def delete_store(id):
    stmt = db.select(Store).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Store not found'}, 404    