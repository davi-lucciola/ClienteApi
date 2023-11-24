from abc import ABC, abstractmethod
from api.domain.models import User


class IUserService(ABC):
    @abstractmethod
    def find_all(self) -> list[User]: ...
    
    @abstractmethod
    def find_by_id(self, id: int) -> User | None: ...

    @abstractmethod
    def create(self, user: User) -> User: ...

    @abstractmethod
    def update(self, user: User) -> User: ...

    @abstractmethod
    def change_password(self, id: int, password: str, new_password: str) -> None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...