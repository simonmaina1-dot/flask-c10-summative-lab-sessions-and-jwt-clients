
# Productivity Notes API - Flask Backend

Secure JWT-based Flask API for user-owned notes. Full CRUD + pagination. Integrates with client-with-jwt frontend.

## IMPORTANT: Always use `pipenv run` (deps in virtualenv only)!

## VSCode Setup
Ctrl+Shift+P → "Python: Select Interpreter" → `/home/sanchez/.local/share/virtualenvs/flask-c10-summative-lab-sessions-and-jwt-c-9h28HwtS/bin/python`

## Installation & Run
1. `pipenv install`
2. `pipenv run python run.py` (creates DB, runs server http://127.0.0.1:5000)
3. `pipenv run python seed.py` (adds test data)

CLI in api/: `cd api && pipenv run FLASK_APP=app.py flask db init/migrate/upgrade` (optional)

Always `pipenv run python file.py` — direct `python file.py` fails (no deps).

API at http://localhost:5000

## Endpoints


### Auth
- `POST /api/auth/register`  
  Body: `{"username": "test", "password": "pass"}`  
  201 created

- `POST /api/auth/login`  
  Body: `{"username": "test", "password": "pass"}`  
  200 logged in, returns JWT access token

- `GET /api/auth/check_session`  
  Auth required (JWT), returns user info if logged in

- `DELETE /api/auth/logout`  
  For JWT: instructs client to delete JWT token (stateless logout)

### Notes (auth required)
- `GET /api/notes?page=1&amp;per_page=5`  
  Paginated user notes only

- `POST /api/notes`  
  Body: `{\"title\": \"My note\", \"content\": \"Details\"}`  
  201 created, owner set

- `PATCH /api/notes/<id>`  
  Body: partial title/content, owner only

- `DELETE /api/notes/<id>`  
  Owner only

## Testing

Use Postman or curl. Pass JWT in Authorization header:

Login:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"youruser","password":"password123"}' http://localhost:5000/api/auth/login
```

Use the returned access_token:
```bash
curl -H "Authorization: Bearer <access_token>" http://localhost:5000/api/notes
```

Logout:
Client should delete the JWT token (stateless logout).

## Errors
400 Bad req, 401 Unauthorized, 403 Unauthorized (owner), 404 Not found.

## Structure
api/ modular blueprints, models, config.
SQLite notes.db.

Ready for Git push/public repo submission.
