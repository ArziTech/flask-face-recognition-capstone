from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.getenv('DATABASE_URL'))

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app