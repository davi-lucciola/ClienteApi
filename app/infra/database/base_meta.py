from ormar import ModelMeta
from app.infra.database import database, metadata


class BaseMeta(ModelMeta):
    database = database
    metadata = metadata