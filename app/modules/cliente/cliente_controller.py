from fastapi import APIRouter
from modules.cliente.cliente import Cliente
from modules.cliente.cliente_use_cases import *


router = APIRouter(prefix='/cliente', tags=['cliente'])


@router.get('/', status_code=HTTPStatus.OK)
async def index():
    clientes = await listar_clientes()
    return clientes

@router.get('/{id}', status_code=HTTPStatus.OK)
async def show(id: int):
    cliente = await buscar_cliente_pelo_id(id)
    return cliente

@router.post('/', status_code=HTTPStatus.CREATED)
async def save(cliente: Cliente):
    return {
        'detail': 'Cliente cadastrado com sucesso.',
        'createdId': await salvar_cliente(cliente)
    }

@router.put('/{id}', status_code=HTTPStatus.CREATED)
async def update(id: int, cliente: Cliente):
    cliente.id = id
    return {
        'detail': 'Cliente cadastrado com sucesso.',
        'createdId': await atualizar_cliente(cliente)
    }

@router.delete('/{id}', status_code=HTTPStatus.ACCEPTED)
async def delete(id: int):
    deletar_cliente(id)
    return {
        'detail': 'Cliente removido com sucesso.'
    }