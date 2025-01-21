from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.Token import Token, TokenRequest
from models.User import UserRequest, UserResponse
from services.UserService import UserService

router = APIRouter(prefix="/user")


@router.post("/login", status_code=200)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends()) -> Token:
    print(form_data)
    return user_service.login_user(form_data)


@router.post("/register", status_code=201)
def register_user(user: UserRequest, user_service: UserService = Depends()) -> UserResponse:
    return user_service.register_user(user)


@router.post("/validate", status_code=200)
def validate_user(token_request: TokenRequest, user_service: UserService = Depends()) -> bool:
    return user_service.validate_user(token_request)
