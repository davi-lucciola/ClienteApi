from http import HTTPStatus
from fastapi import HTTPException
from dataclasses import dataclass
from utils.crypt import CryptService
from models.user import User, UserSave, UserUpdate, UserDTO


@dataclass
class UserService:
    crypt_service: CryptService

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

    async def save(self, user: UserSave) -> int:
        if await self.find_by_email(user.email) is not None:
            raise HTTPException(detail='Email já cadastrado.', status_code=HTTPStatus.BAD_REQUEST)
        
        if user.password != user.confirm_password:
            raise HTTPException(detail='A senha e a sua confimação não são iguais.', status_code=HTTPStatus.BAD_REQUEST)

        user.password = self.crypt_service.hash_password(user.password)

        new_user: User = await User.objects.create(**user.dict(exclude={'confirm_password'}))
        return new_user.id

    async def update(self, user: UserUpdate, user_id: int) -> int:
        user_in_db: User = await self.find_by_id(user_id)

        if (self.find_by_email(user.email) is not None) and (user.email != user_in_db.email):
            raise HTTPException(detail='Email já cadastrado.', status_code=HTTPStatus.BAD_REQUEST)
        
        if self.crypt_service.check_password(user.password, user_in_db.password) is False :
            raise HTTPException(detail='Senha incorreta.', status_code=HTTPStatus.BAD_REQUEST)
        
        if user.new_password != user.confirm_password:
            raise HTTPException(detail='A nova senha e a sua confimação não são iguais.', status_code=HTTPStatus.BAD_REQUEST)

        user.password = self.crypt_service.hash_password(user.new_password)

        return (await user_in_db.update(**user.dict(exclude={'confirm_password', 'new_password'}))).id

    async def delete(self, user_id: int) -> None:
        user: User = await self.find_by_id(user_id)
        await user.delete()

def UserSeviceProvider() -> UserService:
    return UserService(CryptService())