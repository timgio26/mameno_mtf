from flask import Flask
from mameno.extension import migrate,db,jwt
from mameno.models.models import *
from mameno.routes.routes import main_bp
from mameno.routes.error_handler import error_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.register_blueprint(main_bp)
    app.register_blueprint(error_bp)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    return app