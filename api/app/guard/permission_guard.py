# from dataclasses import dataclass
# from fastapi import Depends, Security, HTTPException
# from fastapi.security import HTTPAuthorizationCredentials
# from api.app import HTTPStatus
# from api.app.guard import SECURITY_BEARER, AuthGuard
# from api.domain.models import User, Token, Permission
# from api.domain.services import AuthService, PermissionService

# @dataclass
# class PermissionGuard(AuthGuard):
#     role: str

#     async def __call__(self, 
#         auth_service: AuthService = Depends(AuthService),
#         permission_service: PermissionService = Depends(PermissionService),
#         auth: HTTPAuthorizationCredentials = Security(SECURITY_BEARER)
#     ) -> Token:
#         token: Token = await super().__call__(auth_service, auth)
#         await permission_service.verify_user_permission(token.user.id, self.role)
#         return token
    
#     def __hash__(self) -> int:
#         return hash((type(self),))