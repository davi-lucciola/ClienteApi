import uvicorn
from fastapi import FastAPI
from database import criar_tabelas
from modules.cliente.cliente_controller import router as cliente_controller


app = FastAPI(title='Api Cliente', description='Api para gerenciar clientes')

app.include_router(cliente_controller)

if __name__ == '__main__':
    criar_tabelas()
    uvicorn.run('main:app', host='0.0.0.0', port=9000, reload=True)