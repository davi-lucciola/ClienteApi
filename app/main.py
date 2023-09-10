import uvicorn
from fastapi import FastAPI
from database import criar_tabelas
from modules.user.user_controller import router as user_controller


app = FastAPI(title='Api User Template', description='Template de Usuarios para desenvolver')

app.include_router(user_controller)

if __name__ == '__main__':
    criar_tabelas()
    uvicorn.run('main:app', host='127.0.0.1', port=9000, reload=True)