from dataclasses import dataclass
from api.utils.security import CryptService
from api.domain.models import User
from api.domain.interfaces.services import IUserService
from api.domain.interfaces.repositories import IUserRepository
from api.domain.exceptions import DomainError, NoContentError, NotFoundError


@dataclass
class UserService(IUserService):
    crypt_service: CryptService
    user_repository: IUserRepository

    def find_all(self) -> list[User]:
        users = self.user_repository.find_all()

        if len(users) == 0:
            raise NoContentError()

        return users

    def find_by_id(self, user_id: int) -> User:
        user: User = self.user_repository.find_by_id(user_id)

        if user is None:
            raise NotFoundError('Usuário não encontrado.')
        
        return user

    def create(self, user: User) -> int:
        user.validate_password()

        if self.find_by_email(user.email) is not None and user.id is None:
            raise DomainError('Email já cadastrado.')
        
        user.password = self.crypt_service.hash(user.password)
        
        new_user: User = self.user_repository.save(user)
        return new_user.id

    def update(self, user: User) -> int:
        user_in_db: User = self.find_by_id(user.id)
        
        if self.crypt_service.check_hash(user.password, user_in_db.password) is False:
            raise DomainError('Senha incorreta.')

        user.password = self.crypt_service.hash(user.password)

        return self.user_repository.save(user)

    def find_by_email(self, email: str) -> User | None:
        return self.user_repository.find_by_email(email)
