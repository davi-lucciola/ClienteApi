# from fastapi import APIRouter, Depends
# from api.app import HTTPStatus
# from api.app.guard import AuthGuard
# from api.app.schemas import UserCredentials
# from api.domain.models import Token, User
# from api.domain.services import AuthService


# # Auth Router
# router = APIRouter(prefix='/auth', tags=['Auth'])


# @router.post('/login', status_code = HTTPStatus.OK)
# async def login(credentials: UserCredentials, auth_service: AuthService = Depends(AuthService)):
#     token: str = await auth_service.login(User(**credentials.dict()))
#     return {'acess-token': token, 'type': 'Bearer'}

# @router.put('/refresh')
# async def refresh_token(auth_service: AuthService = Depends(AuthService), token: Token = Depends(AuthGuard())):
#     token: str = await auth_service.refresh_token(token)
#     return {'refresh-token': token, 'type': 'Bearer'}