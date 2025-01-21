from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from services.CategoryService import CategoryService
from services.TokenService import TokenService

router = APIRouter(prefix="/categories")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


@router.get("/", status_code=200)
def get_all_categories(token: str = Depends(oauth2_scheme), token_service: TokenService = Depends(),
                       category_service: CategoryService = Depends()):
    token_service.validate_token(token)
    return category_service.get_all_categories()


@router.get("/{type_transaction}", status_code=200)
def get_all_categories_by_type_transaction(type_transaction: int, token: str = Depends(oauth2_scheme),
                                           token_service: TokenService = Depends(),
                                           category_service: CategoryService = Depends()):
    token_service.validate_token(token)
    return category_service.get_all_categories_by_type_transaction(type_transaction)


@router.get("/{category_id}", status_code=200)
def get_category_by_id(category_id: int, token: str = Depends(oauth2_scheme), token_service: TokenService = Depends(),
                       category_service: CategoryService = Depends()):
    token_service.validate_token(token)
    return category_service.get_category_by_id(category_id)
