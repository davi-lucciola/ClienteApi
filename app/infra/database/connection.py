import decouple as env
from sqlalchemy import MetaData
from databases import Database
from sqlalchemy.engine import Engine, create_engine


DATABASE_URL = env.config('DATABASE_URL')

engine: Engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)
metadata = MetaData(bind=engine)
