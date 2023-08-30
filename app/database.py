import decouple
from ormar import ModelMeta
from sqlalchemy import MetaData
from databases import Database
from sqlalchemy.engine import Engine, create_engine


DATABASE_URL = decouple.config('DATABASE_URL')


engine: Engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)
metadata = MetaData(bind=engine)


class BaseMeta(ModelMeta):
    database = database
    metadata = metadata


def criar_tabelas():
    global metadata, engine
    metadata.create_all(bind=engine)