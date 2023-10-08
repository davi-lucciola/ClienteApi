from fastapi import APIRouter, Depends
from app.api import HTTPStatus, Response
from app.api.guard import AuthGuard, OwnerGuard, PermissionGuard
from app.api.schemas.user import *
from app.domain.models import User, Token
from app.domain.services import UserService

# User Router
router = APIRouter(prefix='/user', tags=['User'])

@router.get('/', status_code = HTTPStatus.OK, dependencies=[Depends(AuthGuard())])
async def index(user_service: UserService = Depends(UserService)) -> list[UserDTO]:
    ''' Endpoint para listar todos os usuarios. '''
    users = await user_service.find_all()
    return users

@router.get('/{id}', status_code = HTTPStatus.OK, dependencies=[Depends(AuthGuard())])
async def show(id: int, user_service: UserService = Depends(UserService)) -> UserDTO:
    ''' Endpoint para detalhar um usuario dado o identificador. '''
    user = await user_service.find_by_id(id)
    return user

@router.post('/secure', status_code = HTTPStatus.CREATED)
async def save_secure(
    user: UserAdmin, 
    user_service: UserService = Depends(UserService), 
    token: Token = Depends(PermissionGuard(':admin'))
):
    ''' 
    Endpoint para cadastrar um usuario. (Autenticação Necessária).
    Somente usuários admin podem cadastrar outros usuários admin.
    '''
    user: User = User(**user.dict(exclude={'confirm_password'}))
    return Response(message='Usuário cadastrado com sucesso.', created_id=await user_service.save(user, token))

@router.post('/public', status_code = HTTPStatus.CREATED)
async def save_public(user: UserSave, user_service: UserService = Depends(UserService)):
    ''' 
    Endpoint para cadastrar um usuario (Autenticação não necessária). 
    '''
    user: User = User(**user.dict(exclude={'confirm_password'}))
    return Response(message='Usuário cadastrado com sucesso.', created_id=await user_service.save(user))

@router.put('/{id}', status_code = HTTPStatus.CREATED)
async def update(id: int, user: UserUpdate, user_service: UserService = Depends(UserService), token: Token = Depends(OwnerGuard(User))):
    ''' 
    Endpoint para atualizar um usuario dado o identificador e os novos dados.
    Somente o próprio usuário ou um usuario admin tem acesso a edição.
    '''
    user: User = User(id=id, **user.dict(exclude={'new_password', 'confirm_new_password'}))
    return Response(message='Usuário editado com sucesso.', created_id=await user_service.update(user, token))

@router.delete('/{id}', status_code = HTTPStatus.ACCEPTED)
async def delete(id: int, user_service: UserService = Depends(UserService), token: Token = Depends(OwnerGuard(User))):
    ''' 
    Endpoint para deletar um usuario dado o identificador.
    Somente o próprio usuário ou um usuario admin tem acesso a remoção.
    '''
    await user_service.delete(id, token)
    return Response(message='Usuário removido com sucesso.')
