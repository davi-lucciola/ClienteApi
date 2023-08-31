from http import HTTPStatus
from fastapi import HTTPException
from dataclasses import dataclass
from modules.cliente import Cliente


@dataclass
class ClienteService:
    async def listar_clientes(self) -> list[Cliente]:
        clientes = await Cliente.objects.all()

        if len(clientes) == 0:
            raise HTTPException(status_code=HTTPStatus.NO_CONTENT)

        return clientes

    async def buscar_cliente_pelo_id(self, cliente_id: int) -> Cliente:
        cliente: Cliente = await Cliente.objects.get_or_none(id = cliente_id)

        if cliente is None:
            raise HTTPException(detail='Cliente não encontrado.', status_code=HTTPStatus.NOT_FOUND)
        
        return cliente

    async def salvar_cliente(self, cliente: Cliente) -> int:
        return (await cliente.save()).id

    async def atualizar_cliente(self, cliente: Cliente) -> int:
        cliente_cadastrado = await self.buscar_cliente_pelo_id(cliente.id)
        return (await cliente_cadastrado.update(**cliente.dict())).id

    async def deletar_cliente(self, cliente_id: int) -> None:
        cliente = await self.buscar_cliente_pelo_id(cliente_id)
        await cliente.delete()