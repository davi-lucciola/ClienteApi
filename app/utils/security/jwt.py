import decouple as env
from jose import jwt
from dataclasses import dataclass


@dataclass
class JwtService:
    ALGORITHM: str = 'HS256'
    TOKEN_SECRET: str = env.config('TOKEN_SECRET') 

    def encode_token(self, payload: dict) -> str:
        return jwt.encode(payload, self.TOKEN_SECRET, self.ALGORITHM)
    
    def decode_token(self, token: str):
        return jwt.decode(token, self.TOKEN_SECRET, algorithms=[self.ALGORITHM])