from fastapi import FastAPI
from app.api.controllers import user_router, auth_router


def create_app(title: str, description: str) -> FastAPI:
    app = FastAPI(title=title, description=description)
   
    # Routes
    app.include_router(auth_router)
    app.include_router(user_router)
    
    app = configure_database(app) 

    return app

def configure_database(app: FastAPI):
    from app.config import database, create_tables
    
    @app.on_event('startup')
    async def startup():
        if not database.is_connected:
            await database.connect()
        create_tables()
    
    @app.on_event('shutdown')
    async def shutdown():
        if database.is_connected:
            await database.disconnect()

    return app