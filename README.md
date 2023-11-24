# User API Template

Template mede with FastAPI and PostgresSQL for develop any system

# Run Local

Having docker installed in your pc, follow the commands:

1. Build api container:
  - `docker compose build`

2. Run db and api containers:
  - `docker compose up -d`

3. Execute migrations:
  - `docker exec -it user_api alembic upgrade head`