from datetime import datetime as dt
from ormar import Model, Integer, String, DateTime, ForeignKey
from app.config import BaseMeta
from app.domain.models import User


class Token(Model):
    class Meta(BaseMeta):
        pass

    id: int = Integer(primary_key=True, autoincrement=True)
    acess_token: str = String(max_length=255, nullable=False)
    initiated_at: dt = DateTime(nullable=False)
    expires_on: dt = DateTime(nullable=False)
    user: User | None = ForeignKey(User, name='user_id', unique=True, nullable=False)