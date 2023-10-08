from datetime import datetime as dt
from ormar import Integer, String, DateTime, ForeignKey
from app.domain.models import User
from app.infra.database import Model, BaseMeta


class Token(Model):
    class Meta(BaseMeta):
        pass

    id: int = Integer(primary_key=True, autoincrement=True)
    acess_token: str = String(max_length=255, nullable=False)
    initiated_at: dt = DateTime(nullable=False)
    expires_on: dt = DateTime(nullable=False)
    user: User | None = ForeignKey(User, name='user_id', unique=True, nullable=False)