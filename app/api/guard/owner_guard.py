from dataclasses import dataclass
from fastapi import Depends, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.api import HTTPStatus
from app.api.guard import SECURITY_BEARER, AuthGuard
from app.domain.models import Model, Token, User
from app.domain.services import AuthService

@dataclass
class OwnerGuard(AuthGuard):
    model: Model

    async def __call__(self, 
        id: int,
        auth_service: AuthService = Depends(AuthService),
        auth: HTTPAuthorizationCredentials = Security(SECURITY_BEARER)
    ) -> Token:
        token: Token = await super().__call__(auth_service, auth)
        token.user = await User.objects.get(id=token.user.id)

        if self.model is User:
            entity: Model = await self.model.objects.get_or_none(id=id)
            if not (token.user.admin is True or token.user.id == entity.id):
                raise HTTPException(detail='Você não tem permissão para acessar este recurso', status_code=HTTPStatus.FORBIDDEN)
        else:
            entity: Model = await self.model.objects.select_related(User).get_or_none(id=id)
            if not (token.user.admin is True or token.user.id == entity.user_id):
                raise HTTPException(detail='Você não tem permissão para acessar este recurso', status_code=HTTPStatus.FORBIDDEN)
        
        return token
    
    def __hash__(self) -> int:
        return hash((type(self),))