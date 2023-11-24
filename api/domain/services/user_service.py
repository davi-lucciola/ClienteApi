from dataclasses import dataclass
from api.utils.security import CryptService
from api.domain.models import User
from api.domain.interfaces.services import IUserService
from api.domain.interfaces.repositories import IUserRepository
from api.domain.errors import DomainError, NoContentError, NotFoundError


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

    def create(self, user: User) -> User:
        user.validate_password()

        if self.user_repository.find_by_email(user.email) is not None:
            raise DomainError('Email já cadastrado.')
        
        user.password = self.crypt_service.hash(user.password)
        new_user: User = self.user_repository.insert(user)
        return new_user

    def update(self, user: User) -> User:
        user_in_db: User = self.find_by_id(user.id)

        if not self.crypt_service.check_hash(user.password, user_in_db.password):
            raise DomainError('Senha incorreta.')

        user_email: User = self.user_repository.find_by_email(user.email)
        if user_email is not None and user_email.id != user.id:
            raise DomainError('Email já cadastrado.')

        user.password = user_in_db.password
        updated_user = self.user_repository.update(user)
        return updated_user
    
    def change_password(self, id: int, password: str, new_password: str) -> None:
        user_in_db: User = self.find_by_id(id)

        if not self.crypt_service.check_hash(password, user_in_db.password):
            raise DomainError('Senha incorreta.')
        
        user_in_db.password = self.crypt_service.hash(new_password)
        self.user_repository.update(user_in_db)
    
    def delete(self, user_id: int) -> None:
        self.find_by_id(user_id)
        self.user_repository.delete(user_id)
