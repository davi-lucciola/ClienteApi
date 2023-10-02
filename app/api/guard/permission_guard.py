# from dataclasses import dataclass
# from fastapi import Path, Depends, Security, HTTPException
# from fastapi.security import HTTPAuthorizationCredentials
# from app.api import HTTPStatus
# from app.api.guard import SECURITY_BEARER, AuthGuard
# from app.domain.models import Token, User, Model
# from app.domain.services import AuthService

# @dataclass
# class PermissionGuard(AuthGuard):
#     permission: str

#     async def __call__(self, 
#         id: int,
#         auth_service: AuthService = Depends(AuthService),
#         auth: HTTPAuthorizationCredentials = Security(SECURITY_BEARER)
#     ) -> Token:
#         token: Token = await super().__call__(auth_service, auth)
#         print(id)
#         return token
#         # model = Model.objects.select_related(User)

#         # if not (token.user.admin is True or token.get('user_id') == user.id):
#         #     raise HTTPException(detail='Você não tem permissão para acessar este recurso', status_code=HTTPStatus.FORBIDDEN)
    
#     def __hash__(self) -> int:
#         return hash((type(self),))