from flask import Blueprint, request
from models.store import Store, StoreSchema
from setup import db
from models.reports import Report, ReportSchema
from flask_jwt_extended import jwt_required
from auth import authorise
from sqlalchemy.exc import IntegrityError



stores_bp = Blueprint('stores', __name__, url_prefix='/stores')

# Get all stores
@stores_bp.route('/', methods=['GET'])
def get_stores():
    # Selects all store tuples from report table using SQLAlchemy Store model
    stmt = db.select(Store)
    # Returns a ScalarResult object with the first value of each result row
    stores = db.session.scalars(stmt).all()
    # Converts object into JSON using Marshmallow StoreSchema, excluding 
    # reports
    return StoreSchema(exclude=['reports'], many=True).dump(stores), 200

# Create a store
@stores_bp.route('/', methods=['POST'])
@jwt_required()
def set_store():
    authorise()
    try:
        # Loads JSON data and converts it to a Marshmallow StoreSchema 
        # instance, excluding any id values retrieved
        store_info = StoreSchema(exclude=['id']).load(request.json)
        # Creates a SQLAlchemy Store instance, retrieving name, address, suburb
        # and state, and attempting to retrieve email, phone_number and 
        # aisle_width, from the Marshmallow StoreSchema instance
        store = Store(
            name = store_info['name'],
            address = store_info['address'],
            suburb = store_info['suburb'],
            state = store_info['state'],
            email = store_info.get('email', ''),
            phone_number = store_info.get('phone_number', None),
            aisle_width = store_info.get('aisle_width', None)
            )
        # Inserts Store instance into the stores table, with SQLAlchemy Store 
        # model translating between Python class variables and SQL values
        db.session.add(store)
        # Commits changes to the database
        db.session.commit()
        # Converts Store instance into JSON using Marshmallow StoreSchema,
        # excluding reports, and dumps 
        return StoreSchema(exclude=['reports']).dump(store), 201
    except IntegrityError:
        return {'error': 'Store with the same name already exists.'}, 409
    except KeyError:
        return {'error': 'Store missing required information.'}, 400


# Update a store
@stores_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_store(id):
    authorise()
    # Loads JSON data and converts it to a Marshmallow StoreSchema instance
    store_info = StoreSchema().load(request.json)
    # Selects from stores table where the route id passed to the function
    # equals the id of a store table tuple using SQLAlchemy Store model
    stmt = db.select(Store).filter_by(id=id)
    # Returns a ScalarResult object with the first value of the first result row
    store = db.session.scalar(stmt)
    # Triggers if ScalarResult object retrieves a matching tuple from stores 
    # table; otherwise, if no matches are found, skips
    if store:
        # Updates ScalarResult object name with name from
        # Marshmallow StoreSchema instance, otherwise defaulting to existing
        # ScalarResult object name
        store.name = store_info.get('name', store.name)
        # Updates ScalarResult object address with address from
        # Marshmallow StoreSchema instance, otherwise defaulting to existing
        # ScalarResult object address
        store.address = store_info.get('address', store.address)
        # Updates ScalarResult object suburb with suburb from
        # Marshmallow StoreSchema instance, otherwise defaulting to existing
        # ScalarResult object suburb
        store.suburb = store_info.get('suburb', store.suburb)
        # Updates ScalarResult object state with state from
        # Marshmallow StoreSchema instance, otherwise defaulting to existing
        # ScalarResult object state
        store.state = store_info.get('state', store.state)
        # Updates ScalarResult object email with email from
        # Marshmallow StoreSchema instance, otherwise defaulting to existing
        # ScalarResult object email
        store.email = store_info.get('email', store.email)
        # Updates ScalarResult object phone_number with phone_number from
        # Marshmallow StoreSchema instance, otherwise defaulting to existing
        # ScalarResult object phone_number
        store.phone_number = store_info.get('phone_number', store.phone_number)
        # Updates ScalarResult object aisle_width with aisle_width from
        # Marshmallow StoreSchema instance, otherwise defaulting to existing
        # ScalarResult object aisle_width
        store.aisle_width = store_info.get('aisle_width', store.aisle_width)
        # Commits changes to the database
        db.session.commit()
        # Converts Store instance into JSON using Marshmallow StoreSchema,
        # excluding reports, and dumps 
        return StoreSchema(exclude=['reports']).dump(store)
    else:
        return {'error': 'Store not found'}, 404

# Delete a store
@stores_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_store(id):
    authorise()
    # Selects from stores table where the route id passed to the function
    # equals the id of a stores table tuple using SQLAlchemy Store model
    stmt = db.select(Store).filter_by(id=id)
    # Returns a ScalarResult object with the first value of the first result row
    user = db.session.scalar(stmt)
    # Triggers if ScalarResult object retrieves a matching tuple from stores 
    # table; otherwise, if no matches are found, skips
    if user:
        # Deletes tuple from stores table
        db.session.delete(user)
        # Commits changes to database
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Store not found'}, 404    
    
# Get a store's reports
@stores_bp.route('/<int:store_id>/reports', methods=['GET'])
@jwt_required()
def get_store_reports(store_id):
    authorise()
    # Selects from reports table where the route id passed to the function
    # equals the store_id of a report table tuple using SQLAlchemy Report model
    stmt = db.select(Report).filter_by(store_id=store_id)
    # Returns a ScalarResult object with the first value of each result row
    reports = db.session.scalars(stmt).all()
    # Converts object into JSON using Marshmallow ReportSchema and dumps
    return ReportSchema(many=True).dump(reports), 200

# Search stores by minimum aisle width
@stores_bp.route('/search', methods=['GET'])
def search_stores():
    # Selects from stores table where the route search arg passed to the 
    # function is more than the aisle_width of a store table tuple using 
    # SQLAlchemy Store model
    stmt = db.select(Store).filter(Store.aisle_width>request.args.get('aisle_width_min'))
    # Returns a ScalarResult object with the first value of each result row
    stores = db.session.scalars(stmt).all()
    # Triggers if ScalarResult object retrieves a matching tuple from reports 
    # table; otherwise, if no matches are found, skips
    if stores:
        # Converts object into JSON using Marshmallow ReportSchema, excluding
        # reports and dumps
        return StoreSchema(many=True, exclude=['reports']).dump(stores), 200
    else:
        return {'error': 'No stores matching search criteria found.'}