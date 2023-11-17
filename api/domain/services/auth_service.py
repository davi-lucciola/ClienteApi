import datetime as dt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from dataclasses import dataclass
from api.app import HTTPStatus
from api.domain.models import User, Token
from api.infra.repositories import Model
from api.utils.security import JwtService, CryptService


@dataclass
class AuthService:
    __EXPIRATION_TIME = dt.timedelta(hours=1)
    jwt_service: JwtService = Depends(lambda: JwtService())
    crypt_service: CryptService = Depends(lambda: CryptService())

    def create_token(self, data: dict, initiated_at: dt, expires_on: dt) -> str:
        token_payload = {
            'exp': expires_on, 
            'iat': initiated_at, 
            **data
        }
        return self.jwt_service.encode_token(token_payload)
    
    async def new_token(self, token_payload: dict) -> str:
        initiated_at: dt = dt.datetime.utcnow() if token_payload.get('iat') is None else token_payload.get('iat')
        expires_on: dt = dt.datetime.utcnow() + self.__EXPIRATION_TIME
        acess_token: str = self.create_token(token_payload, initiated_at, expires_on)

        token: Token = await Token.objects.select_related(Token.user).get_or_none(user__id=token_payload.get('user_id'))
        if token is None:
            token: Token = Token(**{
                'acess_token': acess_token,
                'initiated_at': initiated_at,
                'expires_on': expires_on,
                'user': await User.objects.get(id=token_payload.get('user_id'))
            })
            
        await token.upsert()
        return acess_token

    async def refresh_token(self, token: Token) -> str:
        token_payload: dict = {
            'user_id': token.user.id, 
            'super_user': token.user.super_admin
        }

        return await self.new_token(token_payload)

    async def authenticate(self, auth: HTTPAuthorizationCredentials) -> Token:
        try:
            token_payload: dict = self.jwt_service.decode_token(auth.credentials)
        except ExpiredSignatureError:
            raise HTTPException(detail='Token Expirado.', status_code=HTTPStatus.UNAUTHORIZED)
        except JWTClaimsError:
            raise HTTPException(detail='Token inválido.', status_code=HTTPStatus.UNAUTHORIZED)
        except JWTError:
            raise HTTPException(detail='Token inválido.', status_code=HTTPStatus.UNAUTHORIZED)
        
        token: Token = await Token.objects.get(user_id=token_payload.get('user_id'))
        return token

    async def login(self, credentials: User) -> str:
        user: User = await User.objects.get_or_none(email = credentials.email)
        
        if user is None:
            raise HTTPException(detail='Email não encontrado.', status_code=HTTPStatus.NOT_FOUND)
        
        if not self.crypt_service.check_hash(credentials.password, user.password):
            raise HTTPException(detail='Credenciais Inválidas.', status_code=HTTPStatus.UNAUTHORIZED)

        token_payload: dict = {
            'user_id': user.id, 
            'super_user': user.super_admin
        }

        acess_token: str = await self.new_token(token_payload)
        return acess_token
    
    async def verify_owner(self, resource_id: int, user_id: int, model: Model) -> bool:
        user: User = await User.objects.get(id=user_id)

        if model is User:
            entity: Model = await model.objects.get_or_none(id=resource_id)
            if not (user.super_admin is True or user.id == entity.id): return False
        else:
            entity: Model = await model.objects.select_related(User).get_or_none(id=resource_id)
            if not (user.super_admin is True or user.id == entity.user_id): return False
        
        return True
    