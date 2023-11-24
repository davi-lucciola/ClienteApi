from dataclasses import dataclass
from sqlmodel import Session, select
from api.domain.models import User
from api.domain.interfaces.repositories import IUserRepository
from api.infra.entities import UserEntity


@dataclass
class UserRepository(IUserRepository):
    db: Session

    def find_all(self) -> list[User]: 
        smtm = select(UserEntity)
        results = self.db.exec(smtm).all()
        return [User(**user_entity.dict()) for user_entity in results]
    
    def find_by_id(self, id: int) -> User | None:
        smtm = select(UserEntity).where(UserEntity.id == id)
        user_entity = self.db.exec(smtm).first()
        return User(**user_entity.dict()) if user_entity is not None else None

    def save(self, user: User) -> User: 
        try:
            user_entity = UserEntity(**user.dict())
            self.db.add(user_entity)
            self.db.commit()
            self.db.flush(user_entity)
            return User(**user_entity.dict())
        except Exception as err:
            raise err('Houve um erro ao inserir o usuario.')

    def delete(self, id: int) -> None: 
        user = self.db.exec(select(UserEntity).where(UserEntity.id == id)).first()
        self.db.delete(user)
        self.db.commit()

    def find_by_email(self, email: str) -> User | None:
        return self.db.exec(select(UserEntity).where(UserEntity.email == email)).first()