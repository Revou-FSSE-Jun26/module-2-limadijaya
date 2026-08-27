from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app context
    db.init_app(app)
    migrate.init_app(app, db)

    # Register all routes from separate file
    from app.routes import register_routes
    register_routes(app)

    return app
