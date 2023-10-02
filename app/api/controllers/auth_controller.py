from fastapi import APIRouter, Depends
from app.api import HTTPStatus
from app.api.guard import AuthGuard
from app.domain.models import Token, User, UserCredentials
from app.domain.services import AuthService


# Auth Router
router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/login', status_code = HTTPStatus.OK)
async def login(credentials: UserCredentials, auth_service: AuthService = Depends(AuthService)):
    token: str = await auth_service.login(User(**credentials.dict()))
    return {'acess-token': token, 'type': 'Bearer'}

@router.put('/refresh')
async def refresh_token(auth_service: AuthService = Depends(AuthService), token: Token = Depends(AuthGuard())):
    token: str = await auth_service.refresh_token(token)
    return {'refresh-token': token, 'type': 'Bearer'}