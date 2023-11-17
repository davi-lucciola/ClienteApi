from http import HTTPStatus
from dataclasses import dataclass, field


@dataclass
class NotFoundError(Exception):
    message: str
    status_code: int = field(default=HTTPStatus.NOT_FOUND)