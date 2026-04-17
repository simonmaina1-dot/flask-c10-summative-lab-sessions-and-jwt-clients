import pytest
from api.app import create_app
from api.models import db, User, Note

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def register(client, username, password):
    return client.post('/api/auth/register', json={'username': username, 'password': password})

def login(client, username, password):
    return client.post('/api/auth/login', json={'username': username, 'password': password})

def test_register_and_login(client):
    resp = register(client, 'testuser', 'testpass')
    assert resp.status_code == 201
    resp = login(client, 'testuser', 'testpass')
    assert resp.status_code == 200

def test_check_session(client):
    reg_resp = register(client, 'testuser2', 'testpass')
    assert reg_resp.status_code == 201
    login_resp = login(client, 'testuser2', 'testpass')
    assert login_resp.status_code == 200
    # Session persists automatically in test_client
    resp = client.get('/api/auth/check_session')
    print('check_session resp:', resp.status_code, resp.get_json())
    assert resp.status_code == 200
    assert resp.get_json()['username'] == 'testuser2'

def test_notes_crud(client):
    reg_resp = register(client, 'noteuser', 'pass')
    assert reg_resp.status_code == 201
    login_resp = login(client, 'noteuser', 'pass')
    assert login_resp.status_code == 200
    # Session persists automatically in test_client
    # Create note
    resp = client.post('/api/notes', json={'title': 'T', 'content': 'C'})
    print('notes post resp:', resp.status_code, resp.get_json())
    assert resp.status_code == 201
    note_id = resp.get_json()['id']
    # Get notes
    resp = client.get('/api/notes')
    assert resp.status_code == 200
    assert len(resp.get_json()['notes']) == 1
    note_id = resp.get_json()['notes'][0]['id']
    # Update note
    resp = client.patch(f'/api/notes/{note_id}', json={'title': 'T2'})
    assert resp.status_code == 200
    assert resp.get_json()['title'] == 'T2'
    # Delete note
    resp = client.delete(f'/api/notes/{note_id}')
    assert resp.status_code == 200
    # Confirm gone
    resp = client.get('/api/notes')
    assert len(resp.get_json()['notes']) == 0
