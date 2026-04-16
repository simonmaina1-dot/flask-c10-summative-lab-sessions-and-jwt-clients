from flask import Blueprint, request, jsonify, session
from api.extensions import db
from api.models import User
# Note: db imported directly, User from models (models imports db absolute)

auth_bp = Blueprint('auth', __name__)

def require_auth(f):
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        return f(user_id=user_id, *args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@auth_bp.route('/register', methods=['POST'])
def register():
    data = (request.get_json() or {})
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username taken'}), 400
    
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created', 'user_id': user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = (request.get_json() or {})
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in', 'user_id': user.id}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/check_session', methods=['GET'])
@require_auth
def check_session(user_id):
    user = db.session.get(User, user_id)
    return jsonify({'user_id': user_id, 'username': user.username}), 200

@auth_bp.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out'}), 200

