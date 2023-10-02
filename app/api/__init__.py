from http import HTTPStatus
from pydantic import BaseModel


class Response(BaseModel):
    message: str
    created_id: int | None