from ormar import Integer, String, Boolean, ManyToMany
from app.domain.models import Permission
from app.infra.database import Model, BaseMeta


class User(Model):
    class Meta(BaseMeta):
        pass

    id: int = Integer(primary_key=True, autoincrement=True)
    email: str = String(max_length=255, nullable=False, unique=True)
    password: str = String(max_length=255, nullable=False)
    admin: bool = Boolean(nullable=False, default=False)
    permissions: list[Permission] = ManyToMany(Permission, skip_reverse=True, through_relation_name='user_id', through_reverse_relation_name='permission_id')
