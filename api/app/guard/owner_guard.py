# from dataclasses import dataclass
# from fastapi import Depends, Security, HTTPException
# from fastapi.security import HTTPAuthorizationCredentials
# from api.app import HTTPStatus
# from api.app.guard import SECURITY_BEARER, AuthGuard
# from api.domain.models import Token, User
# from api.domain.services import AuthService
# from api.infra.repositories import Model

# @dataclass
# class OwnerGuard(AuthGuard):
#     model: Model

#     async def __call__(self,
#         id: int,
#         auth_service: AuthService = Depends(AuthService),
#         auth: HTTPAuthorizationCredentials = Security(SECURITY_BEARER)
#     ) -> Token:
#         token: Token = await super().__call__(auth_service, auth)

#         if await auth_service.verify_owner(id, token.user.id, self.model) is False:
#             raise HTTPException(detail='Você não tem permissão para acessar este recurso.', status_code=HTTPStatus.FORBIDDEN)
        
#         return token
    
#     def __hash__(self) -> int:
#         return hash((type(self),))
    