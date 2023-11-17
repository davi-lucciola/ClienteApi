from fastapi import APIRouter, Depends
from api.app import HTTPStatus, Response
from api.app.guard import AuthGuard, PermissionGuard
from api.domain.models import Token, Permission
from api.domain.services import PermissionService


router = APIRouter(prefix='/permission', tags=['Permission'])


@router.get('/my', status_code = HTTPStatus.OK)
async def get_my_permissions(
    permission_service: PermissionService = Depends(PermissionService), 
    token: Token = Depends(AuthGuard())
) -> list[Permission]:
    return await permission_service.my_permissions(token.user.id)

@router.get('/', status_code = HTTPStatus.OK, dependencies=[Depends(PermissionGuard(':admin'))])
async def index(permission_service: PermissionService = Depends(PermissionService)):
    return await permission_service.find_all()

@router.get('/', status_code = HTTPStatus.OK, dependencies=[Depends(PermissionGuard(':admin'))])
async def index(permission_service: PermissionService = Depends(PermissionService)):
    return await permission_service.find_all()

@router.post('/', status_code = HTTPStatus.CREATED, dependencies=[Depends(PermissionGuard(':admin'))])
async def save(permission_service: PermissionService = Depends(PermissionService)):
    pass

@router.put('/{id}', status_code = HTTPStatus.CREATED, dependencies=[Depends(PermissionGuard(':admin'))])
async def update(id: int, permission_service: PermissionService = Depends(PermissionService)):
    pass

@router.delete('/{id}', status_code = HTTPStatus.ACCEPTED, dependencies=[Depends(PermissionGuard(':admin'))])
async def delete(id: int):
    pass