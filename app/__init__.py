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

    # Root health-check / welcome route
    @app.route('/')
    def index():
        from flask import jsonify
        return jsonify({
            'service': 'RevoShop API',
            'status': 'running',
            'endpoints': ['/users', '/auth/login', '/products', '/categories', '/orders']
        }), 200

    return app
