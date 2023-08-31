from database import BaseMeta
from pydantic import BaseModel
from ormar import Model, Integer, String


class Cliente(Model):
    class Meta(BaseMeta):
        pass
    
    id: int | None = Integer(primary_key=True, autoincrement=True)
    nome: str = String(max_length=255, nullable=False)
    email: str = String(max_length=255, nullable=False)
    cpf: str = String(max_length=11, min_length=11, nullable=False)

class ClienteIn(BaseModel):
    nome: str
    email: str
    cpf: str