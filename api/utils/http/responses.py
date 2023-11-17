from dataclasses import dataclass


@dataclass
class Response:
    message: str

@dataclass
class IdResponse(Response):
    created_id: int