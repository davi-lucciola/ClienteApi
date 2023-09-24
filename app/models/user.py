from database import BaseMeta
from pydantic import BaseModel, validator
from email_validator import validate_email, EmailNotValidError
from ormar import Model, Integer, String


class User(Model):
    class Meta(BaseMeta):
        pass
    
    id: int | None = Integer(primary_key=True, autoincrement=True)
    email: str = String(max_length=255, nullable=False, unique=True)
    password: str = String(max_length=255, nullable=False)


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

    @validator('email')
    def email_validation(cls, email: str):
        try:
            validate_email(email)
            return email
        except EmailNotValidError as err:
            raise ValueError(f'Email Inválido, por favor digite um email válido.')

class UserUpdate(UserBase):
    new_password: str
    confirm_new_password: str

class UserDTO(BaseModel):
    id: int
    email: str

class UserCredentials(BaseModel):
    email: str
    password: str
    