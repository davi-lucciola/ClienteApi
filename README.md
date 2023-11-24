# User API Template

Template API mede with FastAPI and PostgresSQL using clean archtecture for develop any system.

## Tests

I have made Unit Tests and Integrated Tests using Pytest.
For the integrated tests i use an sqlite db in memory for simplify and not persist in real database.

## Run Local

Having docker installed in your pc, follow the commands:

1. Build api container:
  - `docker compose build`

2. Run db and api containers:
  - `docker compose up -d`

3. Execute migrations:
  - `docker exec -it user_api alembic upgrade head`