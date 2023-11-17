from api import create_app


user_api = create_app(
    title='User Api Template', 
    description='Api Base para desenvolver sistemas utilizando RBAC'
)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:user_api', host='127.0.0.1', port=9000, reload=True)