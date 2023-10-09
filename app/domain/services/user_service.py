import decouple as env
from string import digits, ascii_lowercase, ascii_uppercase, punctuation 
from fastapi import Depends, HTTPException
from dataclasses import dataclass
from app.api import HTTPStatus
from app.domain.models import User, Permission
from app.utils.security import CryptService


@dataclass
class UserService:
    crypt_service: CryptService = Depends(lambda: CryptService())

    async def find_all(self) -> list[User]:
        users = await User.objects.all()

        if len(users) == 0:
            raise HTTPException(status_code=HTTPStatus.NO_CONTENT)

        return users

    async def find_by_id(self, user_id: int) -> User:
        user: User = await User.objects.get_or_none(id = user_id)

        if user is None:
            raise HTTPException(detail='Usuário não encontrado.', status_code=HTTPStatus.NOT_FOUND)
        
        return user

    async def find_by_email(self, email: str) -> User | None:
        return await User.objects.get_or_none(email = email)

    async def create(self, user: User) -> int:
        if len(user.password) < 4:
            raise HTTPException(detail='Sua senha deve conter pelo menos 4 caracteres.', status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

        have_lower = have_upper = have_special = have_digit = False
        for password_char in user.password:
            if password_char in ascii_lowercase: have_lower = True
            if password_char in ascii_uppercase: have_upper = True
            if password_char in digits: have_digit = True
            if password_char in punctuation: have_special = True
            
        if not have_digit:
            raise HTTPException(detail='Sua senha deve conter numeros.', status_code=HTTPStatus.UNPROCESSABLE_ENTITY)  
        
        if not have_lower:
            raise HTTPException(detail='Sua senha deve conter letras minúsculas.', status_code=HTTPStatus.UNPROCESSABLE_ENTITY)  
        
        if not have_upper:
            raise HTTPException(detail='Sua senha deve conter letras maiúsculas.', status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
        
        if not have_special:
            raise HTTPException(detail='Sua senha deve conter caracteres especiais.', status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
        
        if await self.find_by_email(user.email) is not None and user.id is None:
            raise HTTPException(detail='Email já cadastrado.', status_code=HTTPStatus.BAD_REQUEST)

        new_user: User = await self.save(user)
        return new_user.id

    async def update(self, user: User) -> int:
        user_in_db: User = await self.find_by_id(user.id)
        
        if self.crypt_service.check_hash(user.password, user_in_db.password) is False:
            raise HTTPException(detail='Senha incorreta.', status_code=HTTPStatus.BAD_REQUEST)

        return await self.save(user)

    async def delete(self, user_id: int) -> None:
        user: User = await self.find_by_id(user_id)
        await user.delete()
    
    async def save(self, user: User) -> User:
        user.password: str = self.crypt_service.hash(user.password)
        return user.upsert()

