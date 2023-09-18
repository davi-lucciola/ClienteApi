import decouple
from jose import jwt
from dataclasses import dataclass


@dataclass
class TokenService:
    secret: str = decouple.config('TOKEN_SECRET') 

    @staticmethod
    def create_token():
        return jwt.encode()
    
    @staticmethod
    def validate_token():
        pass