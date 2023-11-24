import decouple as env
from typing import Generator
from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine


DATABASE_URL: str = env.config('DATABASE_URL')
engine: Engine = create_engine(DATABASE_URL)


def get_db() -> Generator[Session, None, None]:
    global engine
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()