from .connection import engine, database, metadata
from .base_meta import BaseMeta
from ormar import Model


def create_tables() -> None:
    global engine, metadata
    metadata.create_all(bind=engine)
