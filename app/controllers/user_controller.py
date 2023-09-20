from fastapi import APIRouter, Depends
from services import UserService
from models import UserSave, UserUpdate, UserDTO
from controllers.responses import ApiResponse, HTTPStatus


router = APIRouter(prefix='/user', tags=['user'])


@router.get('/', status_code = HTTPStatus.OK)
async def index(user_service: UserService = Depends(UserService)) -> list[UserDTO]:
    ''' Endpoint para listar todos os usuarios '''
    users = await user_service.find_all()
    return users

@router.get('/{id}', status_code = HTTPStatus.OK, response_model = UserDTO)
async def show(id: int, user_service: UserService = Depends(UserService)) -> UserDTO:
    ''' Endpoint para detalhar um usuario dado o identificador '''
    user = await user_service.find_by_id(id)
    return user

@router.post('/', status_code = HTTPStatus.CREATED)
async def save(user: UserSave, user_service: UserService = Depends(UserService)):
    ''' Endpoint para cadastrar um usuario. '''
    return ApiResponse(
        message='Usuário cadastrado com sucesso.', 
        created_id=await user_service.save(user)
    )

@router.put('/{id}', status_code = HTTPStatus.CREATED)
async def update(id: int, user: UserUpdate, user_service: UserService = Depends(UserService)):
    ''' Endpoint para atualizar um usuario dado o identificador e os novos dados '''
    return ApiResponse(
        message='Usuário editado com sucesso.', 
        created_id=await user_service.update(user, id)
    )

@router.delete('/{id}', status_code = HTTPStatus.ACCEPTED)
async def delete(id: int, user_service: UserService = Depends(UserService)):
    ''' Endpoint para deletar um usuario dado o identificador'''
    await user_service.delete(id)
    return ApiResponse(message='Usuário removido com sucesso.')
