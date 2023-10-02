import decouple as env
from ormar import ModelMeta
from sqlalchemy import MetaData
from databases import Database
from sqlalchemy.engine import Engine, create_engine


DATABASE_URL = env.config('DATABASE_URL')
TEST_DATABASE = env.config('TEST_DATABASE', False)


engine: Engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL, force_rollback=TEST_DATABASE)
metadata = MetaData(bind=engine)


class BaseMeta(ModelMeta):
    database = database
    metadata = metadata


def create_tables() -> None:
    ''' Cria tabelas no banco de acordo com os modelos mapeados '''
    global metadata, engine
    metadata.create_all(bind=engine)