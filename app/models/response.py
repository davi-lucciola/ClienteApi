from pydantic import BaseModel


class ApiResponse(BaseModel):
    message: str
    created_id: int | None
