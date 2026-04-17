from flask import Blueprint, request, jsonify
from api.extensions import db
from api.models import Note
from api.auth import require_auth

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('', methods=['GET'])
@require_auth
def index(user_id):
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
@require_auth
def create(user_id):
data = request.get_json() or {}
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({'error': 'Title and content required'}), 400
    
    note = Note(title=title, content=content, user_id=user_id)
    db.session.add(note)
    db.session.commit()
    
    return jsonify({'id': note.id, 'title': note.title, 'content': note.content}), 201

@notes_bp.route('/<int:note_id>', methods=['PATCH'])
@require_auth
def update(user_id, note_id):
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'error': 'Note not found or unauthorized'}), 403
    
    data = request.get_json() or {}
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    
    db.session.commit()
    return jsonify({'id': note.id, 'title': note.title, 'content': note.content})

@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@require_auth
def delete(user_id, note_id):
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'error': 'Note not found or unauthorized'}), 403
    
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted'}), 200

if __name__ == '__main__':
    # Legacy standalone run removed: Use `pipenv run python run.py` instead.
    print('Use `pipenv run python run.py` to start the server.')

