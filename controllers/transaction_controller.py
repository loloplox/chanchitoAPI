from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from models.Transaction import TransactionRequest, TransactionUpdateRequest
from services.TokenService import TokenService
from services.TransactionService import TransactionService

router = APIRouter(prefix="/transactions")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


@router.get("/{user_id}", status_code=200)
def get_transactions_of_user(user_id: str, token: str = Depends(oauth2_scheme),
                             transaction_service: TransactionService = Depends(),
                             token_service: TokenService = Depends()):
    token_service.validate_token(token)
    return transaction_service.get_transactions_of_user(user_id)


@router.post("/{user_id}", status_code=201)
def create_transaction_of_user(user_id: str,
                               transaction: TransactionRequest,
                               token: str = Depends(oauth2_scheme),
                               transaction_service: TransactionService = Depends(),
                               token_service: TokenService = Depends()):
    token_service.validate_token(token)
    return transaction_service.create_transaction(transaction, user_id)


@router.put("/{transaction_id}", status_code=200)
def update_transaction_of_user(transaction_id: str,
                               transaction: TransactionUpdateRequest,
                               token: str = Depends(oauth2_scheme),
                               transaction_service: TransactionService = Depends(),
                               token_service: TokenService = Depends()):
    token_service.validate_token(token)
    return transaction_service.update_transaction(transaction, transaction_id)


@router.delete("/{transaction_id}", status_code=200)
def delete_transaction_of_user(transaction_id: str,
                               token: str = Depends(oauth2_scheme),
                               transaction_service: TransactionService = Depends(),
                               token_service: TokenService = Depends()):
    token_service.validate_token(token)
    return transaction_service.delete_transaction(transaction_id)
