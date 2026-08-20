from flask import Blueprint, request, jsonify
from app import db
from app.models import Product, Category, order_items

products_bp = Blueprint('products', __name__)


@products_bp.route('', methods=['GET'])
def get_products():
    """GET /products - List all products."""
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """GET /products/<id> - Get a specific product."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict()), 200


@products_bp.route('', methods=['POST'])
def create_product():
    """POST /products - Create a new product."""
    data = request.get_json() or {}

    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Product name is required'}), 400
    if 'price' not in data or data['price'] is None:
        return jsonify({'error': 'Price is required'}), 400
    if 'category_id' not in data or data['category_id'] is None:
        return jsonify({'error': 'Category ID is required'}), 400

    # Validate price is positive
    try:
        price = float(data['price'])
        if price <= 0:
            return jsonify({'error': 'Price must be greater than zero'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Price must be a valid number'}), 400

    # Validate stock_quantity if provided
    if 'stock_quantity' in data and data['stock_quantity'] is not None:
        try:
            stock = int(data['stock_quantity'])
            if stock < 0:
                return jsonify({'error': 'Stock quantity cannot be negative'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Stock quantity must be a valid integer'}), 400

    # Validate category exists
    category = Category.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    try:
        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            stock_quantity=data.get('stock_quantity', 0),
            category_id=data['category_id']
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify(new_product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """PUT /products/<id> - Update a product."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json() or {}

    # Validate name if provided
    if 'name' in data:
        if not data['name'] or not data['name'].strip():
            return jsonify({'error': 'Product name cannot be empty'}), 400
        product.name = data['name']

    # Validate price if provided
    if 'price' in data:
        try:
            price = float(data['price'])
            if price <= 0:
                return jsonify({'error': 'Price must be greater than zero'}), 400
            product.price = price
        except (ValueError, TypeError):
            return jsonify({'error': 'Price must be a valid number'}), 400

    # Validate stock_quantity if provided
    if 'stock_quantity' in data:
        try:
            stock = int(data['stock_quantity'])
            if stock < 0:
                return jsonify({'error': 'Stock quantity cannot be negative'}), 400
            product.stock_quantity = stock
        except (ValueError, TypeError):
            return jsonify({'error': 'Stock quantity must be a valid integer'}), 400

    # Validate category_id if provided
    if 'category_id' in data:
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        product.category_id = data['category_id']

    if 'description' in data:
        product.description = data['description']

    try:
        db.session.commit()
        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """DELETE /products/<id> - Delete a product (blocked if active orders exist)."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Check if product has active orders (deletion guard)
    active_order_items = db.session.execute(
        order_items.select().where(order_items.c.product_id == product_id)
    ).fetchall()

    if active_order_items:
        return jsonify({
            'error': 'Cannot delete product with active orders. Remove associated orders first.'
        }), 400

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
