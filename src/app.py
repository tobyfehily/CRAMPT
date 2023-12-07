from setup import app
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users_bp
from blueprints.stores_bp import stores_bp
from blueprints.reports_bp import reports_bp
from marshmallow.exceptions import ValidationError


app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(stores_bp)
app.register_blueprint(reports_bp)

@app.errorhandler(404)
def not_found_error(err):
    return {'error': 'Page not found.'}, 404

@app.errorhandler(ValidationError)
def validation_error(err):
    return {'error': str(err)}, 400

@app.errorhandler(401)
def authorisation_error(err):
    return {'error': 'You are not authorised to perform this action.'}, 401

@app.errorhandler(405)
def method_not_allowed(err):
    return {'error': 'This HTTP method is not supported on this URL.'}, 405

@app.errorhandler(400)
def authorisation_error(err):
    return {'error': "It's not me, it's you – you've made some kind of mistake."}, 401


print(app.url_map)