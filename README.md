# BudoWay API - Full features

Includes:
- SQLModel models (auto-generated from your SQL)
- CRUD routers (GET open; POST/PUT/DELETE protected by JWT)
- Simple JWT auth endpoints (/auth/register and /auth/token)
- Alembic scaffold for migrations (configure sqlalchemy.url in alembic.ini)
- export_openapi.py to dump OpenAPI JSON/YAML
- example JSON payloads in /examples

## Setup (macOS)

1. Create venv and install deps
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create DB and import schema (optional)
```
createdb budowaydb
psql -U postgres -d budowaydb -f /path/to/BudoWayDB.sql
```

3. Set env vars
```
export DATABASE_URL="postgresql://postgres:password@localhost:5432/budowaydb"
export SECRET_KEY="change_this_to_a_secure_value"
```

4. Run app
```
uvicorn budoway_api.main:app --reload
```

5. Register auth user (example)
```
curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d '{"email":"me@example.com","password":"secret"}'
```

6. Use token to create resources (Authorization: Bearer <token>)
```
curl -X POST http://localhost:8000/events -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d @examples/events_create.json
```

7. Alembic
- configure `alembic.ini` sqlalchemy.url to your DATABASE_URL
- run migrations
```
alembic upgrade head
```

8. Export OpenAPI
```
python export_openapi.py
```