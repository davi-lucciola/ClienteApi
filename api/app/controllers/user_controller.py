from fastapi import APIRouter, Depends
from api.utils.http import HTTPStatus, Response, ResponseWithId
from api.app import UserServiceDependency
# from api.app.guard import AuthGuard, OwnerGuard, PermissionGuard
from api.app.schemas.user import *
from api.domain.models import User
from api.domain.interfaces.services import IUserService


# User Router
router = APIRouter(prefix='/user', tags=['User'])


@router.get('/', status_code = HTTPStatus.OK) # dependencies=[Depends(AuthGuard())]
async def index(user_service: IUserService = Depends(UserServiceDependency)) -> list[UserDTO]:
    ''' Endpoint para listar todos os usuarios. '''
    users = user_service.find_all()
    return users

@router.get('/{id}', status_code = HTTPStatus.OK) # dependencies=[Depends(AuthGuard())]
async def show(id: int, user_service: IUserService = Depends(UserServiceDependency)) -> UserDTO:
    ''' Endpoint para detalhar um usuario dado o identificador. '''
    user = user_service.find_by_id(id)
    return user

# @router.post('/secure', status_code = HTTPStatus.CREATED) # dependencies=[Depends(PermissionGuard(':admin'))]
# async def create_secure(user: UserAdmin, user_service: IUserService = Depends(UserServiceDependency)):
#     ''' 
#     Endpoint para cadastrar um usuario. (Autenticação Necessária).
#     Somente usuários admin podem cadastrar outros usuários admin.
#     '''
#     user: User = User(**user.dict(exclude={'confirm_password'}))
#     return ResponseWithId(message='Usuário cadastrado com sucesso.', created_id=user_service.create(user).id)

@router.post('/public', status_code = HTTPStatus.CREATED, response_model=ResponseWithId)
async def create_public(user: UserCreate, user_service: IUserService = Depends(UserServiceDependency)):
    ''' 
    Endpoint para cadastrar um usuario (Autenticação não necessária). 
    '''
    user: User = User(**user.dict(exclude={'confirm_password'}))
    return ResponseWithId(message='Usuário cadastrado com sucesso.', created_id=user_service.create(user).id)

@router.put('/{id}', status_code = HTTPStatus.CREATED)
async def update(
    id: int, 
    user: UserAdmin, 
    # token: Token = Depends(OwnerGuard(User)), 
    user_service: IUserService = Depends(UserServiceDependency)
) -> Response:
    ''' 
    Endpoint para atualizar um usuario dado o identificador e os novos dados (Não troca a senha). 
    Somente o próprio usuário ou um usuario admin tem acesso a edição.
    '''
    updated_user: User = User(id=id, **user.dict(exclude={'new_password', 'confirm_new_password'}))
    return ResponseWithId(message='Usuário editado com sucesso.', created_id=user_service.update(updated_user).id)

@router.post('/{id}/change-password', status_code = HTTPStatus.CREATED)
async def change_password(
    id: int,
    credentials: UserChangePassword,
    # token: Token = Depends(OwnerGuard(User)), 
    user_service: IUserService = Depends(UserServiceDependency)
) -> Response:
    ''' 
    Endpoint para trocar a senha do usuario.
    Somente o proprio usuario ou usuario admin pode trocar a senha.
    '''
    user_service.change_password(id, credentials.password, credentials.new_password)
    return Response(message='Senha atualizada com sucesso')

@router.delete('/{id}', status_code = HTTPStatus.ACCEPTED) # dependencies=[Depends(OwnerGuard(User))]
async def delete(id: int, user_service: IUserService = Depends(UserServiceDependency)):
    ''' 
    Endpoint para deletar um usuario dado o identificador.
    Somente o próprio usuário ou um usuario admin tem acesso a remoção.
    '''
    user_service.delete(id)
    return Response(message='Usuário removido com sucesso.')
