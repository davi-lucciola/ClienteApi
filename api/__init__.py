'''
API de Template com as funcionalidades:

- Cadastro de Usuarios Publicos e Admins
- Controle de Acesso com Autenticação
- Sistema de Permissões
'''
from fastapi import FastAPI
from api.app.controllers import *


def create_app(title: str, description: str) -> FastAPI:
    app = FastAPI(title=title, description=description)
   
    # Routes
    # app.include_router(auth_router)
    app.include_router(user_router)
    # app.include_router(permission_router)
    
    return app