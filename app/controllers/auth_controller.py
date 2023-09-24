from fastapi import APIRouter, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from controllers import HTTPStatus
from models import UserCredentials
from services import UserService, UserServiceProvider, AuthService, AuthServiceProvider


# Security
SECURITY_BEARER = HTTPBearer() 
async def authenticate(
    auth_service: AuthService = Depends(AuthServiceProvider),
    auth: HTTPAuthorizationCredentials = Security(SECURITY_BEARER)
) -> dict:
    return await auth_service.authenticate(auth)


# Auth Router
router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/login', status_code = HTTPStatus.OK)
async def login(credentials: UserCredentials, user_service: UserService = Depends(UserServiceProvider)):
    token: str = await user_service.login(credentials)
    return {'acess-token': token, 'type': 'Bearer'}

@router.put('/refresh')
async def refresh_token(auth_service: AuthService = Depends(AuthServiceProvider), token: dict = Depends(authenticate)):
    token: str = await auth_service.refresh_token(token)
    return {'refresh-token': token, 'type': 'Bearer'}