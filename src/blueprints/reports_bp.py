from flask import Blueprint, request
from setup import db
from models.reports import Report, ReportSchema

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

# Get all reports
@reports_bp.route('/', methods=['GET'])
def get_reports():
    stmt = db.select(Report)
    reports = db.session.scalars(stmt).all()
    return ReportSchema(many=True).dump(reports)

# Get a report
@reports_bp.route('/<int:id>', methods=['GET'])
def get_report(id):
    stmt = db.select(Report).filter_by(id=id)
    report = db.session.scalar(stmt)
    print(request.host)
    if report:
        return ReportSchema().dump(report), 200
    else:
        return {'error': 'Report not found'}, 404

# Update a report
@reports_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_report(id):
    report_info = ReportSchema().load(request.json)
    stmt = db.select(Report).filter_by(id=id)
    report = db.session.scalar(stmt)
    if report:
        report.aisle_width = report_info.get('aisle_width', report.aisle_width),
        report.image = report_info.get('image', report.image),
        report.store_id  = report_info.get('store_id', report.store_id),
        db.session.commit()
        return ReportSchema().dump(report)
    else:
        return {'error': 'Report not found'}, 404

# Delete a report
@reports_bp.route('/<int:id>', methods=['DELETE'])
def delete_report(id):
    stmt = db.select(Report).filter_by(id=id)
    report = db.session.scalar(stmt)
    if report:
        db.session.delete(report)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Report not found'}, 404   
    

# Create a report
@reports_bp.route('/', methods=['POST'])
def create_report():
    report_info = ReportSchema().load(request.json)
    report = Report(
        aisle_width = report_info['aisle_width'],
        image = report_info.get('image'),
        store_id = report_info['store_id'],
        user_id = report_info['user_id']
        )
    db.session.add(report)
    db.session.commit()
    return ReportSchema().dump(report), 201
    