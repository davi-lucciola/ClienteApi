import decouple as env
from fastapi import FastAPI
from app.api.controllers import *
from app.domain.models import User, Permission
from app.infra.database import database, create_tables
from app.utils.security import CryptService


def create_app(title: str, description: str) -> FastAPI:
    app = FastAPI(title=title, description=description)
   
    # Routes
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(permission_router)
    
    app = configure_database(app) 

    return app

async def initial_super_user():
    ADMIN_ROLE = ':admin'
    if await User.objects.get_or_none(super_admin=True) is None:
        user: User = User(
            email=env.config('SUPERUSER_EMAIL'), 
            password=CryptService().hash(env.config('SUPERUSER_PASSWORD')), 
            super_admin=True
        )

        await user.save()
        await user.permissions.add(await Permission.objects.get_or_create(role=ADMIN_ROLE))
        await user.save_related()

def configure_database(app: FastAPI):
    @app.on_event('startup')
    async def startup():
        if not database.is_connected:
            await database.connect()
        
        create_tables()
        # await initial_super_user()
    
    @app.on_event('shutdown')
    async def shutdown():
        if database.is_connected:
            await database.disconnect()

    return app