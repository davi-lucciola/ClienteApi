from abc import ABC, abstractmethod
from api.domain.models import User


class IUserRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[User]: ...
    
    @abstractmethod
    def find_by_id(self, id: int) -> User | None: ...

    @abstractmethod
    def save(self, user: User) -> User: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...

    @abstractmethod
    def find_by_email(self, email: str) -> User | None: ...