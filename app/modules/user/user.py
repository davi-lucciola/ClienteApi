from database import BaseMeta
from pydantic import BaseModel, validate_email, validator
from ormar import Model, Integer, String


class User(Model):
    class Meta(BaseMeta):
        pass
    
    id: int | None = Integer(primary_key=True, autoincrement=True)
    email: str = String(max_length=255, nullable=False)
    password: str = String(max_length=255, nullable=False)

class UserSave(BaseModel):
    email: str
    password: str
    confirm_password: str

    @validator('email')
    def email_validation(cls, email: str):
        print(email)
        raise ValueError('Testando Validações: Email')

class UserUpdate(UserSave):
    new_password: str