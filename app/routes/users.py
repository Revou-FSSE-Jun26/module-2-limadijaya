from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app import db
from app.models import User

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['POST'])
def register_user():
    """POST /users - Register a new user."""
    data = request.get_json() or {}

    # Validate mandatory inputs
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields: username, email, password'}), 400

    # Ensure email uniqueness
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User with this email already exists'}), 409

    # Hash the password using werkzeug
    password_hash = generate_password_hash(data['password'])

    try:
        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=password_hash,
            role=data.get('role', 'customer')
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """GET /users/<id> - Fetch user by ID."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200
