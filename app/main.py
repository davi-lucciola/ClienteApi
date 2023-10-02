import uvicorn
from app import create_app

user_api = create_app('User Api Template', 'Api Base para desenvolver sistemas utilizando RBAC')

if __name__ == '__main__':
    uvicorn.run('main:user_api', host='127.0.0.1', port=9000, reload=True)