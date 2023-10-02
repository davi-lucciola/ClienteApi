from dataclasses import dataclass
from fastapi import Depends, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.api import HTTPStatus
from app.api.guard import SECURITY_BEARER, AuthGuard
from app.domain.models import User, Token, Permission
from app.domain.services import AuthService, PermissionService

@dataclass
class PermissionGuard(AuthGuard):
    permission: str

    async def __call__(self, 
        auth_service: AuthService = Depends(AuthService),
        permission_service: PermissionService = Depends(PermissionService),
        auth: HTTPAuthorizationCredentials = Security(SECURITY_BEARER)
    ) -> Token:
        token: Token = await super().__call__(auth_service, auth)

        user: User = await User.objects.get(id=token.user.id)
        permissions: list[Permission] = await permission_service.find_all_user_permissions(token.user.id)
        user_roles: list[str] = [permission.role for permission in permissions]
        
        if not (user.admin is True or self.permission in user_roles):
            raise HTTPException(detail='Você não tem permissão para acessar esse recurso.', status_code=HTTPStatus.FORBIDDEN)
        
        return token
    
    def __hash__(self) -> int:
        return hash((type(self),))