import uvicorn
from fastapi import FastAPI
from database import create_tables
from controllers import user_router


app = FastAPI(title='Api User Template', description='Template de Usuarios para desenvolver')

app.include_router(user_router)

if __name__ == '__main__':
    create_tables()
    uvicorn.run('main:app', host='127.0.0.1', port=9000, reload=True)