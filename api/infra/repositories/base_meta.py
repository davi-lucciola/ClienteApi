from ormar import ModelMeta
from api.infra.repositories import database, metadata


class BaseMeta(ModelMeta):
    database = database
    metadata = metadata