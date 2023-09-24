from fastapi import APIRouter, Depends
from services import UserService, UserServiceProvider
from controllers import HTTPStatus, Auth
from models import Response, User, UserSave, UserUpdate, UserDTO, UserCredentials


router = APIRouter(prefix='/user', tags=['User'])


@router.get('/', status_code = HTTPStatus.OK)
async def index(user_service: UserService = Depends(UserServiceProvider)) -> list[UserDTO]:
    ''' Endpoint para listar todos os usuarios '''
    users = await user_service.find_all()
    return users

@router.get('/{id}', status_code = HTTPStatus.OK, dependencies=[Depends(Auth)])
async def show(id: int, user_service: UserService = Depends(UserServiceProvider)) -> User:
    ''' Endpoint para detalhar um usuario dado o identificador '''
    user = await user_service.find_by_id(id)
    return user

@router.post('/', status_code = HTTPStatus.CREATED, dependencies=[Depends(Auth)])
async def save(user: UserSave, user_service: UserService = Depends(UserServiceProvider)):
    ''' Endpoint para cadastrar um usuario. '''
    return Response(message='Usuário cadastrado com sucesso.', created_id=await user_service.save(user))

@router.put('/{id}', status_code = HTTPStatus.CREATED, dependencies=[Depends(Auth)])
async def update(id: int, user: UserUpdate, user_service: UserService = Depends(UserServiceProvider)):
    ''' Endpoint para atualizar um usuario dado o identificador e os novos dados '''
    return Response(message='Usuário editado com sucesso.', created_id=await user_service.update(user, id))

@router.delete('/{id}', status_code = HTTPStatus.ACCEPTED, dependencies=[Depends(Auth)])
async def delete(id: int, user_service: UserService = Depends(UserServiceProvider)):
    ''' Endpoint para deletar um usuario dado o identificador'''
    await user_service.delete(id)
    return Response(message='Usuário removido com sucesso.')

