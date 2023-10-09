from http import HTTPStatus
from pydantic import BaseModel


class Response(BaseModel):
    detail: str
    created_id: int | None