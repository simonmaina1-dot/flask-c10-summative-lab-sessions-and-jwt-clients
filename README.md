# Productivity Notes API - Flask Backend

Secure session-based Flask API for user-owned notes. Full CRUD + pagination. Integrates with client-with-sessions frontend.

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
  Body: `{\"username\": \"test\", \"password\": \"pass\"}`  
  201 created

- `POST /api/auth/login`  
  Body: `{\"username\": \"test\", \"password\": \"pass\"}`  
  200 logged in, sets session cookie

- `GET /api/auth/check_session`  
  Auth req, returns user info if logged in

- `DELETE /api/auth/logout`  
  Clears session

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
Use Postman (save cookies) or curl:

Login:
```bash
curl -X POST -H "Content-Type: application/json" -d '{\"username\":\"youruser\",\"password\":\"password123\"}' -c cookies.txt http://localhost:5000/api/auth/login
```

Notes:
```bash
curl -X GET -b cookies.txt "http://localhost:5000/api/notes?page=1&amp;per_page=3"
```

## Errors
400 Bad req, 401 Unauthorized, 403 Unauthorized (owner), 404 Not found.

## Structure
api/ modular blueprints, models, config.
SQLite notes.db.

Ready for Git push/public repo submission.
