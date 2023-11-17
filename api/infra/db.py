import decouple as env
from sqlalchemy.engine import Engine, create_engine

DATABASE_URL = env.config('DATABASE_URL')

engine: Engine = create_engine(DATABASE_URL)

def create_tables() -> None:
    global engine
    metadata.create_all(bind=engine)