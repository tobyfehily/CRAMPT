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
    stmt = db.select(Report)
    reports = db.session.scalars(stmt).all()
    return ReportSchema(many=True).dump(reports)

# Create a report
@reports_bp.route('/', methods=['POST'])
@jwt_required()
def create_report():
    try:
        report_info = ReportSchema().load(request.json)
        report = Report(
            aisle_width = report_info['aisle_width'],
            image = report_info.get('image'),
            store_id = report_info['store_id'],
            user_id = get_jwt_identity()
            )
        db.session.add(report)
        db.session.commit()
        return ReportSchema(exclude=['user_id']).dump(report), 201
    except KeyError:
        return {'error': 'Report missing required information.'}, 400

# Update a report
@reports_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_report(id):
    report_info = ReportSchema().load(request.json)
    stmt = db.select(Report).filter_by(id=id)
    report = db.session.scalar(stmt)
    if report:
        authorise(report.user_id)
        report.aisle_width = report_info.get('aisle_width', report.aisle_width),
        report.image = report_info.get('image', report.image),
        report.store_id  = report_info.get('store_id', report.store_id),
        db.session.commit()
        return ReportSchema(exclude=['user_id']).dump(report)
    else:
        return {'error': 'Report not found'}, 404

# Delete a report
@reports_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_report(id):
    stmt = db.select(Report).filter_by(id=id)
    report = db.session.scalar(stmt)
    if report:
        authorise(report.user_id)
        db.session.delete(report)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Report not found'}, 404