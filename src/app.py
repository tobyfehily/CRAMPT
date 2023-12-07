from setup import app
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users_bp
from blueprints.stores_bp import stores_bp

app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(stores_bp)