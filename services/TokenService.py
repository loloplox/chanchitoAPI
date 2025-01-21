import time

import jwt
from decouple import config
from fastapi import HTTPException

from models.User import User


class TokenService:
    def __init__(self):
        self.SECRET_KEY = config("JWT_SECRET_KEY")
        self.ALGORITHM = config("JWT_ALGORITHM")
        self.EXPIRE_TOKEN = 60 * 60 * 24

    def create_token(self, data: User) -> str:
        to_encode = {"sub": data.username}
        time_expire = time.time() + self.EXPIRE_TOKEN

        to_encode.update({"exp": time_expire})
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return encode_jwt

    def decode_token(self, token: str) -> dict:
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        return payload

    def validate_token(self, token: str) -> dict:
        try:
            payload = self.decode_token(token)

            if payload["exp"] < time.time() and not payload["sub"]:
                raise jwt.ExpiredSignatureError

            username = payload["sub"]

            return {"token_valid": True, "username": username}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token, {e.args}")
