from http import HTTPStatus
from fastapi import HTTPException
from modules.cliente.cliente import Cliente


async def listar_clientes() -> list[Cliente]:
    clientes = await Cliente.objects.all()

    if len(clientes) == 0:
        raise HTTPException(status_code=HTTPStatus.NO_CONTENT)

    return clientes

async def buscar_cliente_pelo_id(cliente_id: int) -> Cliente:
    cliente: Cliente = await Cliente.objects.get_or_none(id = cliente_id)

    if cliente is None:
        raise HTTPException(detail='Cliente não encontrado.', status_code=HTTPStatus.NOT_FOUND)
    
    return cliente

async def salvar_cliente(cliente: Cliente) -> int:
    return (await cliente.save()).id

async def atualizar_cliente(cliente: Cliente) -> int:
    await buscar_cliente_pelo_id(cliente.id)
    return await salvar_cliente(cliente)

async def deletar_cliente(cliente_id: int) -> None:
    cliente = await buscar_cliente_pelo_id(cliente_id)
    await cliente.delete()