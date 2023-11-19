import decouple as env
from typing import Generator
from contextlib import contextmanager
from sqlmodel import Session, create_engine


DATABASE_URL = env.config('DATABASE_URL')
engine = create_engine(DATABASE_URL)


@contextmanager
def get_session(commit: bool = True) -> Generator[Session, None, None]:
    global engine
    session = Session(bind=engine)
    try:
        yield session
    finally:
        if commit is True: session.commit()
        else: session.rollback()

        session.close()


def get_db() -> Generator[Session, None, None]:
    with get_session() as session:
        yield session


def get_test_db() -> Generator[Session, None, None]:
    with get_session(commit=False) as session:
        yield session