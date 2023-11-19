from http import HTTPStatus
from dataclasses import dataclass, field
from api.domain.exceptions import DomainError


@dataclass
class NotFoundError(DomainError):
    message: str
    status_code: int = field(default=HTTPStatus.NOT_FOUND)