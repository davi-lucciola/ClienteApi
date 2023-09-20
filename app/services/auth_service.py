from http import HTTPStatus
from fastapi import HTTPException
from dataclasses import dataclass, field
from models import UserCredentials, User
from services import UserService
from utils.security import JwtService


@dataclass
class AuthService:
    jwt_service: JwtService = field(default_factory=lambda: JwtService())
    user_service: UserService = field(default_factory=lambda: UserService())

    async def login(self, credentials: UserCredentials):
        user: User = await self.user_service.find_by_email(credentials.email)
        
        if user is None:
            raise HTTPException(detail='Email não encontrado.', status_code=HTTPStatus.NOT_FOUND)
        
        if not self.user_service.crypt_service.check_password(credentials.password, user.password):
            raise HTTPException(detail='Credenciais Inválidas.', status_code=HTTPStatus.UNAUTHORIZED)

        return self.__create_token(user.id) 

    def __create_token(self, user_id: int) -> str:
        token = {
            'exp': 1,
            'int': 2,
            'user_id': user_id
        }
        
