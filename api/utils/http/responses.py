from dataclasses import dataclass


@dataclass
class Response:
    message: str

@dataclass
class ResponseWithId(Response):
    created_id: int