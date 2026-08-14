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

    # Import and register blueprints
    from app.routes.products import products_bp
    from app.routes.users import users_bp

    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(users_bp, url_prefix='/users')

    return app