from pydantic import BaseModel, validator
from email_validator import validate_email, EmailNotValidError


class UserCredentials(BaseModel):
    email: str
    password: str

    @validator('email')
    def email_validation(cls, email: str):
        try:
            validate_email(email)
            return email
        except EmailNotValidError as err:
            raise ValueError(f'Email Inválido, por favor digite um email válido.')

class UserSave(UserCredentials):
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, confirm_password: str, values: dict):
        if confirm_password != values.get('password'):
            raise ValueError(f'As senha e a confirmação não são iguais.')

class UserAdmin(UserSave):
    admin: bool = False

class UserUpdate(UserCredentials):
    admin: bool = False
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
