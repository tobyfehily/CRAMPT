from flask import Blueprint, request
from models.store import Store, StoreSchema
from setup import db
from models.reports import Report, ReportSchema
from flask_jwt_extended import jwt_required
from auth import authorise


stores_bp = Blueprint('stores', __name__, url_prefix='/stores')

# Get all stores
@stores_bp.route('/', methods=['GET'])
def get_stores():
    stmt = db.select(Store)
    stores = db.session.scalars(stmt).all()
    return StoreSchema(exclude=['reports'], many=True).dump(stores), 200

# Create a store
@stores_bp.route('/', methods=['POST'])
@jwt_required()
def set_store():
    authorise()
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
    return StoreSchema(exclude=['reports']).dump(store), 201

# Update a store
@stores_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_store(id):
    authorise()
    store_info = StoreSchema().load(request.json)
    print(store_info)
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

# Delete a store
@stores_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_store(id):
    authorise()
    stmt = db.select(Store).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Store not found'}, 404    
    
# Get a store's reports
@stores_bp.route('/<int:store_id>/reports', methods=['GET'])
@jwt_required()
def get_store_reports(store_id):
    authorise()
    stmt = db.select(Report).filter_by(store_id=store_id)
    reports = db.session.scalars(stmt).all()
    return ReportSchema(many=True).dump(reports), 200

# Search stores
@stores_bp.route('/search', methods=['GET'])
def search_stores():
    stmt = db.select(Store).filter(Store.aisle_width>request.args.get('aisle_width_min'))
    stores = db.session.scalars(stmt).all()
    print(stores)
    if stores == []:
        return {'error': 'No stores matching search criteria found.'}
    else:
        return StoreSchema(many=True, exclude=['reports']).dump(stores), 200