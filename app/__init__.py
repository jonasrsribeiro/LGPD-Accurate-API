from flask import Flask
from config import Config
from app.routes import bp as routes_bp

from app.database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(routes_bp, url_prefix='/api')

    return app