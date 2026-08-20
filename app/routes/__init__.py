from app.routes.products import products_bp
from app.routes.users import users_bp
from app.routes.categories import categories_bp
from app.routes.orders import orders_bp
from app.routes.auth import auth_bp


def register_routes(app):
    """Register all application blueprints."""
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(auth_bp, url_prefix='/auth')
