from pydantic import BaseModel, EmailStr
from string import digits, ascii_lowercase, ascii_uppercase, punctuation 


class User(BaseModel):
    id: int | None
    email: EmailStr
    password: str 
    admin: bool

    def validate_password(self):
        if len(self.password) < 4:
            raise ValueError('Sua senha deve conter pelo menos 4 caracteres.')
        
        have_lower = have_upper = have_special = have_digit = False
        for password_char in self.password:
            if password_char in ascii_lowercase: have_lower = True

            if password_char in ascii_uppercase:  have_upper = True
            if password_char in digits: have_digit = True
            if password_char in punctuation: have_special = True
            
        if not have_digit:
            raise ValueError('Sua senha deve conter numeros.')
            
        if not have_lower:
            raise ValueError('Sua senha deve conter letras minúsculas.')
            
        if not have_upper:
            raise ValueError('Sua senha deve conter letras maiúsculas.')
        
        if not have_special:
            raise ValueError('Sua senha deve conter caracteres especiais.')
