import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Blueprint, request, jsonify, session
from functools import wraps
from api.extensions import db
from api.models import User

auth_bp = Blueprint('auth', __name__)

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id_str = session.get('user_id')
        if not user_id_str:
            return jsonify({'error': 'Unauthorized'}), 401
        try:
            user_id = int(user_id_str)
        except ValueError:
            return jsonify({'error': 'Unauthorized'}), 401
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
    
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    session['user_id'] = str(user.id)
    return jsonify({'id': user.id, 'username': user.username}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = str(user.id)
        return jsonify({'id': user.id, 'username': user.username}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    user_id_str = session.get('user_id')
    if not user_id_str:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        user_id = int(user_id_str)
    except ValueError:
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user_id': user_id, 'username': user.username}), 200

@auth_bp.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out'}), 200
