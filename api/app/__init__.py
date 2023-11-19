from fastapi import Depends
from sqlmodel import Session
from api.utils.security import CryptService
from api.domain.services import UserService
from api.infra.connections import get_db
from api.infra.repositories import UserRepository


def UserServiceDependency(db: Session = Depends(get_db)):
    return UserService(CryptService(), UserRepository(db)) 