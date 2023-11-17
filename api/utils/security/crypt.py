from dataclasses import dataclass, field
from passlib.context import CryptContext 


@dataclass
class CryptService:
    pwd_context: CryptContext = field(default_factory=lambda: CryptContext(schemes=['bcrypt'], deprecated='auto'))

    def hash(self, plain_text: str) -> str:
        return self.pwd_context.hash(plain_text)

    def check_hash(self, plain_text: str, hash: str) -> bool:
        return self.pwd_context.verify(plain_text, hash)
