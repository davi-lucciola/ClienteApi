from http import HTTPStatus
from dataclasses import dataclass, field


@dataclass
class DomainError(Exception):
    message: str
    status_code: int = field(default=HTTPStatus.BAD_REQUEST)