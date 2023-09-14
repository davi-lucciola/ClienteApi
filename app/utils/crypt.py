from dataclasses import dataclass, field
from passlib.context import CryptContext 


@dataclass
class CryptService:
    pwd_context: CryptContext = field(default_factory=lambda: CryptContext(schemes=['bcrypt'], deprecated='auto'))

    def hash_password(self, password) -> str:
        return self.pwd_context.hash(password)

    def check_password(self, password, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

