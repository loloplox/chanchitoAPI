from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError

from models.Token import Token, TokenRequest
from models.User import UserRequest, UserResponse
from repositories.UserRepository import UserRepository
from services.PasswordService import PasswordService
from services.TokenService import TokenService


class UserService:
    def __init__(self, user_repository: UserRepository = Depends(),
                 password_service: PasswordService = Depends(),
                 token_service: TokenService = Depends()):
        self.user_repository = user_repository
        self.password_service = password_service
        self.token_service = token_service

    def login_user(self, user_request: OAuth2PasswordRequestForm) -> Token:
        user = self.user_repository.get_user_by_username(username=user_request.username)

        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        if not self.password_service.verify_password(user_request.password, user.password):
            raise HTTPException(status_code=401, detail="La contraseña no es valida")

        if not user.active:
            raise HTTPException(status_code=401, detail="El usurio no esta activo")

        token = self.token_service.create_token(user)

        return Token(access_token=token, token_type="bearer", username=user.username, user_id=user.id)

    def register_user(self, user: UserRequest) -> UserResponse:
        password_hash = self.password_service.get_password_hash(user.password)
        user.password = password_hash

        try:
            self.user_repository.create_user(user)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=400, detail=str(e.args[0]))

        user_created = self.user_repository.get_user_by_username(user.username)

        return UserResponse(id=user_created.id, username=user_created.username, active=user_created.active)

    def validate_user(self, token_request: TokenRequest) -> bool:
        result = self.token_service.validate_token(token=token_request.access_token)

        token_valid = result["token_valid"]
        username = result["username"]

        user_found = self.user_repository.get_user_by_username(username)

        if user_found:
            if not user_found.active:
                raise HTTPException(status_code=401, detail="El usuario no esta abilitado")
            else:
                return token_valid
        else:
            return False
