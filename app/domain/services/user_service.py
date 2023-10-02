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

    async def save(self, user: User, token: dict = {}) -> int:
        if await self.find_by_email(user.email) is not None and user.id is None:
            raise HTTPException(detail='Email já cadastrado.', status_code=HTTPStatus.BAD_REQUEST)

        user.password = self.crypt_service.hash(user.password)

        admin_permission = await Permission.objects.get_or_create(role=':admin')
        if user.admin is True:
            user.permissions.add(admin_permission)
        else:
            user.permissions.remove(admin_permission)
        
        print(user.permissions)
        new_user: User = await user.upsert(**user.dict())
        print(new_user.permissions)
        return new_user.id

    async def update(self, user: User, token: dict) -> int:
        user_in_db: User = await self.find_by_id(user.id)
        
        if self.crypt_service.check_hash(user.password, user_in_db.password) is False:
            raise HTTPException(detail='Senha incorreta.', status_code=HTTPStatus.BAD_REQUEST)

        return await self.save(user)

    async def delete(self, user_id: int, token: dict) -> None:
        user: User = await self.find_by_id(user_id)

        if not (token.get('admin') is True or token.get('user_id') == user.id):
            raise HTTPException(detail='Você não tem permissão para deletar esse usuario', status_code=HTTPStatus.FORBIDDEN)

        await user.delete()
