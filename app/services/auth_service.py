import datetime as dt
from http import HTTPStatus
from fastapi import HTTPException
from utils.security import JwtService
from dataclasses import dataclass, field
from fastapi.security import HTTPAuthorizationCredentials
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError


@dataclass
class AuthService:
    EXPIRATION_TIME: dt.timedelta = dt.timedelta(hours=1)
    jwt_service: JwtService = field(default_factory=lambda: JwtService())

    def create_token(self, data: dict) -> str:
        expiration_time = dt.datetime.utcnow() + self.EXPIRATION_TIME
        token_payload = {'exp': expiration_time, 'iat': dt.datetime.utcnow(), **data}
        return self.jwt_service.encode_token(token_payload)
    
    async def authenticate(self, auth: HTTPAuthorizationCredentials) -> dict:
        try:
            token_payload: dict = self.jwt_service.decode_token(auth.credentials)
        except ExpiredSignatureError:
            raise HTTPException(detail='Token Expirado.', status_code=HTTPStatus.UNAUTHORIZED)
        except JWTClaimsError:
            raise HTTPException(detail='Token inválido.', status_code=HTTPStatus.UNAUTHORIZED)
        except JWTError:
            raise HTTPException(detail='Token inválido.', status_code=HTTPStatus.UNAUTHORIZED)
        
        return token_payload
    
    async def refresh_token(self, token: dict):
        token['exp'] = dt.datetime.utcnow() + self.EXPIRATION_TIME
        return self.jwt_service.encode_token(token)

def AuthServiceProvider() -> AuthService:
    return AuthService()