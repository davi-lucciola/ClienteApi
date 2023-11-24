from sqlmodel import SQLModel, Field


class UserEntity(SQLModel, table=True):
    __tablename__ = 'user'

    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str 
    admin: bool = Field(default=False)
