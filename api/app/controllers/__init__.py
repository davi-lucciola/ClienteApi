from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.utils.http import HTTPStatus
from api.domain.errors import DomainError
from .user_controller import router as user_router
# from .auth_controller import router as auth_router
# from .permission_controller import router as permission_router


def handle_domain_error(request: Request, error: DomainError):
    if error.message is not None:
        body = {'message': error.message}
    else:
        body = None

    return JSONResponse(content=body, status_code=error.status_code)

def handle_value_error(request: Request, error: ValueError):
    body = {'message': error.args[0]}
    return JSONResponse(content=body, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

def handle_request_validation_error(request: Request, error: RequestValidationError):
    body = {'message': error.args[0][0]['msg']}
    return JSONResponse(content=body, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

def handle_internal_server_error(request: Request, error: Exception):
    body = {'error': str(error.__cause__)}
    return JSONResponse(content=body, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)