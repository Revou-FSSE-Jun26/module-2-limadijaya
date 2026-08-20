from flask import Blueprint, request, jsonify
from app import db
from app.models import Category

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('', methods=['GET'])
def get_categories():
    """GET /categories - List all categories."""
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories]), 200


@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """GET /categories/<id> - Get a specific category with its products."""
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(category.to_dict(include_products=True)), 200


@categories_bp.route('', methods=['POST'])
def create_category():
    """POST /categories - Create a new category."""
    data = request.get_json() or {}

    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400

    # Check uniqueness
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category with this name already exists'}), 409

    try:
        new_category = Category(
            name=data['name'],
            description=data.get('description', '')
        )

        db.session.add(new_category)
        db.session.commit()

        return jsonify(new_category.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """PUT /categories/<id> - Update a category."""
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    data = request.get_json() or {}

    if 'name' in data:
        if not data['name'] or not data['name'].strip():
            return jsonify({'error': 'Category name cannot be empty'}), 400
        # Check uniqueness if name is changing
        existing = Category.query.filter_by(name=data['name']).first()
        if existing and existing.id != category_id:
            return jsonify({'error': 'Category with this name already exists'}), 409
        category.name = data['name']

    if 'description' in data:
        category.description = data['description']

    try:
        db.session.commit()
        return jsonify(category.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """DELETE /categories/<id> - Delete a category."""
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
