from flask import Blueprint, request
from setup import db
from models.reports import Report, ReportSchema

reports_bp = Blueprint('reports', __name__)
user_reports_bp = Blueprint('user_reports', __name__)

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
    if report:
        return ReportSchema().dump(report), 200
    else:
        return {'error': 'Report not found'}, 404

# Get a user's reports
@user_reports_bp.route('/', methods=['GET'])
def get_user_reports(id):
    stmt = db.select(Report).filter_by(user_id=id)
    reports = db.session.scalars(stmt).all()
    return ReportSchema(many=True).dump(reports), 200


# # Search reports
# @reports_bp.route('/search', methods=['GET'])
# def search_reports():
#     if request.args.get('store_id'):
#         stmt = db.select(Report).filter_by(store_id=request.args.get('store_id'))
#         reports = db.session.scalars(stmt).all()
#         print(reports)
#         if reports == []:
#             return {'error': 'No reports matching store id found.'}
#         else:
#             return ReportSchema(many=True).dump(reports), 200
    
#     if request.args.get('user_id'):
#         stmt = db.select(Report).filter_by(user_id=request.args.get('user_id'))
#         reports = db.session.scalars(stmt).all()
#         print(reports)
#         if reports == []:
#             return {'error': 'No reports matching user id found.'}
#         else:
#             return ReportSchema(many=True).dump(reports), 200
