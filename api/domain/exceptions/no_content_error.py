from http import HTTPStatus
from dataclasses import dataclass, field


@dataclass
class NoContentError(Exception):
    status_code: int = field(default=HTTPStatus.NO_CONTENT)