from http import HTTPStatus
from dataclasses import dataclass, field
from api.domain.exceptions import DomainError


@dataclass
class NoContentError(DomainError):
    message: str = None
    status_code: int = field(default=HTTPStatus.NO_CONTENT)