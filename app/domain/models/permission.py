'''
As permissões funcionam da seguinte forma:

-> model:permission-type

Tipos de Permissões:
- read
- save
- update
- delete
- admin (nao tem modelo associado, é só ":admin")

Um usuario terá varias roles.
'''
from ormar import Integer, String
from app.infra.database import Model, BaseMeta


class Permission(Model):
    class Meta(BaseMeta):
        pass

    id: int | None = Integer(primary_key=True, autoincrement=True)
    role: str = String(max_length=255, nullable=False)
