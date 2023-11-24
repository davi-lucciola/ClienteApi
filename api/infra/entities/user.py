from sqlmodel import SQLModel, Field


class UserEntity(SQLModel, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password: str 
    admin: bool = Field(default=False)