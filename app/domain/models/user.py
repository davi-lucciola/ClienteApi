from pydantic import BaseModel, validator
from email_validator import validate_email, EmailNotValidError
from ormar import Model, Integer, String, Boolean, ManyToMany
from app.config import BaseMeta
from app.domain.models import Permission


class User(Model):
    class Meta(BaseMeta):
        pass

    id: int = Integer(primary_key=True, autoincrement=True)
    email: str = String(max_length=255, nullable=False, unique=True)
    password: str = String(max_length=255, nullable=False)
    admin: bool = Boolean(nullable=False, default=False)
    permissions = ManyToMany(Permission, skip_reverse=True, through_relation_name='user_id', through_reverse_relation_name='permission_id')

class UserBase(BaseModel):
    email: str
    password: str

    @validator('email')
    def email_validation(cls, email: str):
        try:
            validate_email(email)
            return email
        except EmailNotValidError as err:
            raise ValueError(f'Email Inválido, por favor digite um email válido.')

class UserSave(UserBase):
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, confirm_password: str, values: dict):
        if confirm_password != values.get('password'):
            raise ValueError(f'As senha e a confirmação não são iguais.')

class UserAdmin(UserSave):
    admin: bool = False

class UserUpdate(UserBase):
    new_password: str
    confirm_new_password: str

    @validator('confirm_new_password')
    def passwords_match(cls, confirm_new_password: str, values: dict):
        if confirm_new_password != values.get('new_password'):
            raise ValueError(f'As senha e a confirmação não são iguais.')

class UserDTO(BaseModel):
    id: int
    email: str
    admin: bool

class UserCredentials(BaseModel):
    email: str
    password: str
    