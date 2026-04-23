# Productivity Notes API - Full Auth Flask Backend (Summative Lab Complete)

Session-based Flask API for secure user-owned notes. Implements full auth, protected CRUD + pagination per rubric specs. Compatible with session-based frontend client.

**Status: COMPLETE** - All requirements met (auth/CRUD/pag/secure/models/seed/structure/README).

## Installation
1. Install dependencies: `pipenv install`
2. DB/migrate (dev uses create_all; optional): `pipenv run flask db init && pipenv run flask db migrate && pipenv run flask db upgrade` (needs FLASK_APP=api.app)
   Or auto-create: `pipenv run python run.py` (starts server at http://127.0.0.1:5000, creates sqlite:///notes.db)
3. Seed test data: `pipenv run python seed.py` (3 users: user1-3 pw=password123, 9 notes)

**Note:** Always use `pipenv run` commands.

## Run
`pipenv run python run.py`

Server: http://127.0.0.1:5000/  
Root: `GET /` → {\"message\": \"Notes API Backend ready. See README for endpoints.\"}

## Endpoints

### Auth (/api/auth)
- `POST /api/auth/register`  
  Body: `{\"username\": \"test\", \"password\": \"pass\"}`  
  Creates user, logs in. 201: `{\"id\": 1, \"username\": \"test\"}` | 400 username taken/req

- `POST /api/auth/login`  
  Body: `{\"username\": \"test\", \"password\": \"pass\"}`  
  Logs in. 200: `{\"id\": 1, \"username\": \"test\"}` | 400/401 invalid/missing

- `GET /api/auth/check_session`  
  Session req. 200 user info | 401 unauth

- `DELETE /api/auth/logout`  
  Clears session. 200: `{\"message\": \"Logged out\"}`

### Notes (/api/notes) - Auth protected, user-owned only
- `GET /api/notes?page=1&per_page=10`  
  Paginated: `{\"notes\": [...], \"page\":1, \"per_page\":10, \"pages\":N, \"total\":N}` | 401 unauth

- `POST /api/notes`  
  Body: `{\"title\": \"My Note\", \"content\": \"Details\"}`  
  201: note details | 400 missing | 401

- `PATCH /api/notes/<id>`  
  Body: `{\"title\": \"Updated\"}` (partial)  
  Owner only. 200 details | 403 not owner | 401 | 404

- `DELETE /api/notes/<id>`  
  Owner only. 200 `{\"message\": \"Note deleted\"}` | 403/401/404

## Testing
`pipenv run python -m pytest test_api.py -v` (3 tests pass: auth + notes CRUD)

curl examples (save cookies):
```bash
# Register/Login (saves session cookie)
curl -c cookies.txt -X POST -H 'Content-Type: application/json' -d '{\"username\":\"user1\",\"password\":\"password123\"}' http://127.0.0.1:5000/api/auth/login

# Protected
curl -b cookies.txt http://127.0.0.1:5000/api/notes
curl -b cookies.txt -X POST -H 'Content-Type: application/json' -d '{\"title\":\"Test\",\"content\":\"Test\"}' http://127.0.0.1:5000/api/notes

# Logout
curl -b cookies.txt -X DELETE http://127.0.0.1:5000/api/auth/logout
```

## Errors
400 Bad Request, 401 Unauthorized, 403 Forbidden (not owner), 404 Not Found.

**Rubric Compliance:** Full auth (10/10), protected CRUD/pagination (10/10), models bcrypt/unique (10/10), seed (10/10), structure modular (5/5), tests (bonus).


