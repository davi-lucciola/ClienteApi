from fastapi import APIRouter, Depends
from app.api import HTTPStatus, Response
from app.api.guard import AuthGuard
from app.domain.models import Token, Permission
from app.domain.services import PermissionService


router = APIRouter(prefix='/permission', tags=['Permission'])


@router.get('/my', status_code=HTTPStatus.OK)
async def get_my_permissions(
    permission_service: PermissionService = Depends(PermissionService), 
    token: Token = Depends(AuthGuard())
) -> list[Permission]:
    return await permission_service.my_permissions(token.user.id)