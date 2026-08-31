from flask import Blueprint, request, jsonify
from app import db
from app.models import Order, Product, User, order_items

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('', methods=['POST'])
def create_order():
    """POST /orders - Place a new order linked to the logged-in user."""
    data = request.get_json() or {}

    # Validate user_id
    if not data.get('user_id'):
        return jsonify({'error': 'user_id is required'}), 400

    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Validate items
    if not data.get('items') or not isinstance(data['items'], list) or len(data['items']) == 0:
        return jsonify({'error': 'Order must contain at least one item'}), 400

    try:
        # Calculate total and validate products
        total_amount = 0
        validated_items = []

        for item in data['items']:
            if not item.get('product_id'):
                return jsonify({'error': 'Each item must have a product_id'}), 400

            product = Product.query.get(item['product_id'])
            if not product:
                return jsonify({'error': f"Product with id {item['product_id']} not found"}), 404

            quantity = item.get('quantity', 1)
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be greater than zero'}), 400

            unit_price = float(product.price)
            total_amount += unit_price * quantity

            validated_items.append({
                'product_id': product.id,
                'quantity': quantity,
                'unit_price': unit_price
            })

        # Create the order
        new_order = Order(
            user_id=data['user_id'],
            status=data.get('status', 'pending'),
            total_amount=total_amount
        )

        db.session.add(new_order)
        db.session.flush()  # Get the order ID

        # Insert order items
        for item in validated_items:
            db.session.execute(
                order_items.insert().values(
                    order_id=new_order.id,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price']
                )
            )

        db.session.commit()

        return jsonify(new_order.to_dict(include_items=True)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orders_bp.route('', methods=['GET'])
def get_orders():
    """GET /orders - List all orders.

    Returns the full list of orders by default. If a user_id query
    parameter is provided, the list is filtered to that user's orders.
    """
    user_id = request.args.get('user_id', type=int)

    if user_id:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        orders = Order.query.filter_by(user_id=user_id).all()
    else:
        orders = Order.query.all()

    return jsonify([order.to_dict() for order in orders]), 200


@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """GET /orders/<id> - View a specific order with its order items and product details."""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order.to_dict(include_items=True)), 200


@orders_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """PUT /orders/<id> - Update an existing order (status)."""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    data = request.get_json() or {}

    if 'status' in data:
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400
        order.status = data['status']

    try:
        db.session.commit()
        return jsonify(order.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """DELETE /orders/<id> - Delete an order."""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    try:
        # Delete order items first
        db.session.execute(
            order_items.delete().where(order_items.c.order_id == order_id)
        )
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
