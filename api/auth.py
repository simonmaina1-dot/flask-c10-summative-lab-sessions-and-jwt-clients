# JWT logout is stateless; for completeness, provide a /logout endpoint that instructs client to delete token
@auth_bp.route('/logout', methods=['DELETE'])
def logout():
    return jsonify({'message': 'Logout: client should delete JWT token'}), 200
from flask import Blueprint, request, jsonify
from functools import wraps
from api.extensions import db, jwt
from api.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

auth_bp = Blueprint('auth', __name__)

def require_auth(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = int(get_jwt_identity())
        return f(user_id=user_id, *args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username taken'}), 400
    
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'message': 'User created', 'user_id': user.id, 'access_token': access_token}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'Logged in', 'user_id': user.id, 'access_token': access_token}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/check_session', methods=['GET'])
@require_auth
def check_session(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user_id': user_id, 'username': user.username}), 200

