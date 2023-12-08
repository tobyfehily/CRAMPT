from flask import Blueprint, request
from setup import db
from models.reports import Report, ReportSchema
from auth import authorise
from flask_jwt_extended import jwt_required, get_jwt_identity


reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

# Get all reports
@reports_bp.route('/', methods=['GET'])
@jwt_required()
def get_reports():
    authorise()
    # Selects all report tuples from report table using SQLAlchemy Report model
    stmt = db.select(Report)
    # Returns a ScalarResult object with the first value of each result row
    reports = db.session.scalars(stmt).all()
    # Converts object into JSON using Marshmallow ReportSchema and dumps
    return ReportSchema(many=True).dump(reports)

# Create a report
@reports_bp.route('/', methods=['POST'])
@jwt_required()
def create_report():
    try:
        # Loads JSON data and converts it to a Marshmallow ReportSchema 
        # instance, excluding any date_created values retrieved
        report_info = ReportSchema(exclude=['date_created']).load(request.json)
        # Creates a SQLAlchemy Report instance, retrieving aisle_Width and 
        # store_id, and attempting to retrieve image, from the Marshmallow 
        # ReportSchema instance, and retrieving user_id from the supplied
        # JWT token payload's sub
        report = Report(
            aisle_width = report_info['aisle_width'],
            image = report_info.get('image'),
            store_id = report_info['store_id'],
            user_id = get_jwt_identity()
            )
        # Inserts Report instance into the reports table, with SQLAlchemy Report 
        # model translating between Python class variables and SQL values
        db.session.add(report)
        # Commits changes to the database
        db.session.commit()
        # Converts Report instance into JSON using Marshmallow ReportSchema,
        # excluding user_id, and dumps 
        return ReportSchema(exclude=['user_id']).dump(report), 201
    except KeyError:
        return {'error': 'Report missing required information.'}, 400

# Update a report
@reports_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_report(id):
    # Loads JSON data and converts it to a Marshmallow ReportSchema instance, 
    # excluding any date_created values retrieved
    report_info = ReportSchema(exclude=['date_created']).load(request.json)
    # Selects from reports table where the route id passed to the function
    # equals the id of a report table tuple using SQLAlchemy Report model
    stmt = db.select(Report).filter_by(id=id)
    # Returns a ScalarResult object with the first value of the first result row
    report = db.session.scalar(stmt)
    # Triggers if ScalarResult object retrieves a matching tuple from reports 
    # table; otherwise, if no matches are found, skips
    if report:
        authorise(report.user_id)
        # Updates ScalarResult object aisle_width with aisle_width from
        # Marshmallow ReportSchema instance, otherwise defaulting to existing
        # ScalarResult object aisle_width
        report.aisle_width = report_info.get('aisle_width', report.aisle_width)
        # Updates ScalarResult object image with image from
        # Marshmallow ReportSchema instance, otherwise defaulting to existing
        # ScalarResult object image
        report.image = report_info.get('image', report.image)
        # Updates ScalarResult object store_id with store_id from
        # Marshmallow ReportSchema instance, otherwise defaulting to existing
        # ScalarResult object store_id
        report.store_id  = report_info.get('store_id', report.store_id)
        # Commits changes to the database
        db.session.commit()
        # Converts Report instance into JSON using Marshmallow ReportSchema,
        # excluding user_id, and dumps 
        return ReportSchema(exclude=['user_id']).dump(report)
    else:
        return {'error': 'Report not found'}, 404

# Delete a report
@reports_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_report(id):
    # Selects from reports table where the route id passed to the function
    # equals the id of a report table tuple using SQLAlchemy Report model
    stmt = db.select(Report).filter_by(id=id)
    # Returns a ScalarResult object with the first value of the first result row
    report = db.session.scalar(stmt)
    # Triggers if ScalarResult object retrieves a matching tuple from reports 
    # table; otherwise, if no matches are found, skips
    if report:
        authorise(report.user_id)
        # Deletes tuple from reports table
        db.session.delete(report)
        # Commits changes to database
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Report not found'}, 404