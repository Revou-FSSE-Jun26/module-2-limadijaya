from flask import Blueprint, jsonify

products_bp = Blueprint('products', __name__)

# Hardcoded product list
HARDCODED_PRODUCTS = [
    {
        "id": 1,
        "name": "Wireless Noise-Canceling Headphones",
        "description": "High quality audio over-ear headphones",
        "price": 199.99,
        "stock_quantity": 50
    },
    {
        "id": 2,
        "name": "Mechanical Gaming Keyboard",
        "description": "RGB backlight with blue switches",
        "price": 89.50,
        "stock_quantity": 100
    },
    {
        "id": 3,
        "name": "Classic Cotton T-Shirt",
        "description": "100% organic cotton unisex tee",
        "price": 24.99,
        "stock_quantity": 200
    }
]

@products_bp.route('', methods=['GET'])
def get_products():
    """GET /products - Retrieve full hardcoded list."""
    return jsonify(HARDCODED_PRODUCTS), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """GET /products/<id> - Retrieve single product by ID."""
    product = next((p for p in HARDCODED_PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200