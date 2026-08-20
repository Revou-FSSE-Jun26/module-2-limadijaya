from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """POST /auth/login - Authenticate user."""
    data = request.get_json() or {}

    # Validate required fields
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields: email, password'}), 400

    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    # Verify password using werkzeug
    if not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    }), 200
