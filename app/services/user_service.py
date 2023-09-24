from http import HTTPStatus
from fastapi import HTTPException
from services.auth_service import AuthService
from utils.security import CryptService
from dataclasses import dataclass, field
from models.user import User, UserSave, UserUpdate, UserCredentials


@dataclass
class UserService:
    auth_service: AuthService = field(default_factory=lambda: AuthService())
    crypt_service: CryptService = field(default_factory=lambda: CryptService())

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

        user.password = self.crypt_service.hash(user.password)

        new_user: User = await User.objects.create(**user.dict(exclude={'confirm_password'}))
        return new_user.id

    async def update(self, user: UserUpdate, user_id: int) -> int:
        user_in_db: User = await self.find_by_id(user_id)

        if (await self.find_by_email(user.email) is not None) and (user.email != user_in_db.email):
            raise HTTPException(detail='Email já cadastrado.', status_code=HTTPStatus.BAD_REQUEST)
        
        if self.crypt_service.check_hash(user.password, user_in_db.password) is False:
            raise HTTPException(detail='Senha incorreta.', status_code=HTTPStatus.BAD_REQUEST)
        
        if user.new_password != user.confirm_new_password:
            raise HTTPException(detail='A nova senha e a sua confimação não são iguais.', status_code=HTTPStatus.BAD_REQUEST)

        user.password = self.crypt_service.hash(user.new_password)

        return (await user_in_db.update(**user.dict(exclude={'confirm_new_password', 'new_password'}))).id

    async def delete(self, user_id: int) -> None:
        user: User = await self.find_by_id(user_id)
        await user.delete()
    
    async def login(self, credentials: UserCredentials) -> str:
        user: User = await self.find_by_email(credentials.email)
        
        if user is None:
            raise HTTPException(detail='Email não encontrado.', status_code=HTTPStatus.NOT_FOUND)
        
        if not self.crypt_service.check_hash(credentials.password, user.password):
            raise HTTPException(detail='Credenciais Inválidas.', status_code=HTTPStatus.UNAUTHORIZED)

        return self.auth_service.create_token({'user_id': user.id})

def UserServiceProvider() -> UserService:
    return UserService()