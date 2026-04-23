import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.extensions import db
from api.models import Note

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('', methods=['GET'])
@jwt_required()
def index():
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    notes = Note.query.filter_by(user_id=user_id)\
                     .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'notes': [{'id': n.id, 'title': n.title, 'content': n.content} for n in notes.items],
        'page': page,
        'per_page': per_page,
        'pages': notes.pages,
        'total': notes.total
    })

@notes_bp.route('', methods=['POST'])
@jwt_required()
def create():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({'errors': ['Title and content required']}), 400
    
    note = Note(title=title, content=content, user_id=user_id)
    db.session.add(note)
    db.session.commit()
    
    return jsonify({'id': note.id, 'title': note.title, 'content': note.content}), 201

@notes_bp.route('/<int:note_id>', methods=['PATCH'])
@jwt_required()
def update(note_id):
    user_id = int(get_jwt_identity())
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'errors': ['Note not found or unauthorized']}), 403
    
    data = request.get_json() or {}
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    
    db.session.commit()
    return jsonify({'id': note.id, 'title': note.title, 'content': note.content})

@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete(note_id):
    user_id = int(get_jwt_identity())
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'errors': ['Note not found or unauthorized']}), 403
    
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted'}), 200

