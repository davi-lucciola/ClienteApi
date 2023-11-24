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
    
    def insert(self, user: User) -> User:
        user_entity = UserEntity(**user.dict())
        try:
            self.db.add(user_entity)
            self.db.commit()
        except:
            self.db.rollback()
            raise Exception('Houve um erro ao cadastrar o usuário')
        
        self.db.refresh(user_entity)
        return User(**user_entity.dict())
       
    def update(self, user: User) -> User:
        user_entity = self.db.exec(select(UserEntity).where(UserEntity.id == user.id)).one()
        try:
            user_entity.email = user.email
            user_entity.password = user.password
            user_entity.admin = user.admin

            self.db.commit()
        except:
            self.db.rollback()
            raise Exception('Houve um erro ao atualizar o usuário')
        
        self.db.refresh(user_entity)
        return User(**user_entity.dict())

    def delete(self, id: int) -> None: 
        user = self.db.exec(select(UserEntity).where(UserEntity.id == id)).one()
        try:
            self.db.delete(user)
            self.db.commit()
        except Exception as err:
            self.db.rollback()
            raise Exception('Houve um erro ao deletar o usuário.', str(err))

    def find_by_email(self, email: str) -> User | None:
        return self.db.exec(select(UserEntity).where(UserEntity.email == email)).first()
