from http import HTTPStatus
from fastapi import APIRouter, Depends
from modules.cliente import *


router = APIRouter(prefix='/cliente', tags=['cliente'])


@router.get('/', status_code = HTTPStatus.OK)
async def index(cliente_service: ClienteService = Depends(ClienteService)) -> list[Cliente]:
    ''' Endpoint para listar todos os clientes '''
    clientes = await cliente_service.listar_clientes()
    return clientes

@router.get('/{id}', status_code = HTTPStatus.OK)
async def show(id: int, cliente_service: ClienteService = Depends(ClienteService)) -> Cliente:
    ''' Endpoint para detalhar um cliente dado o identificador '''
    cliente = await cliente_service.buscar_cliente_pelo_id(id)
    return cliente

@router.post('/', status_code = HTTPStatus.CREATED)
async def save(cliente: ClienteIn, cliente_service: ClienteService = Depends(ClienteService)):
    ''' Endpoint para cadastrar um cliente. '''
    cliente = Cliente(**cliente.dict())
    return {
        'detail': 'Cliente cadastrado com sucesso.',
        'createdId': await cliente_service.salvar_cliente(cliente)
    }

@router.put('/{id}', status_code = HTTPStatus.CREATED)
async def update(id: int, cliente: Cliente, cliente_service: ClienteService = Depends(ClienteService)):
    ''' Endpoint para atualizar um cliente dado o identificador e os novos dados '''
    cliente.id = id
    return {
        'detail': 'Cliente editado com sucesso.',
        'createdId': await cliente_service.atualizar_cliente(cliente)
    }

@router.delete('/{id}', status_code = HTTPStatus.ACCEPTED)
async def delete(id: int, cliente_service: ClienteService = Depends(ClienteService)):
    ''' Endpoint para deletar um cliente dado o identificador'''
    cliente_service.deletar_cliente(id)
    return {
        'detail': 'Cliente removido com sucesso.'
    }