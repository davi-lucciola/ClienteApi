import decouple
from jose import jwt
from dataclasses import dataclass


@dataclass
class JwtService:
    ALGORITHM: str = 'HS256'
    TOKEN_SECRET: str = decouple.config('TOKEN_SECRET') 

    def generate(self, payload: dict) -> str:
        return jwt.encode(payload, self.TOKEN_SECRET, self.ALGORITHM)
    
    def validate(self, token):
        return jwt.decode(token, self.TOKEN_SECRET, self.ALGORITHM)