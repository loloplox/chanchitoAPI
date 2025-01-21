from fastapi.params import Depends

from models.Transaction import TransactionRequest, TransactionUpdateRequest
from repositories.TransactionRepository import TransactionRepository


class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository = Depends()):
        self.transaction_repository = transaction_repository

    def get_transactions_of_user(self, user_id: str):
        return self.transaction_repository.get_transactions_by_user_id(user_id)

    def create_transaction(self, transaction: TransactionRequest, user_id: str):
        return self.transaction_repository.create_transaction(transaction, user_id)

    def update_transaction(self, transaction: TransactionUpdateRequest, transaction_id: str):
        return self.transaction_repository.update_transaction(transaction, transaction_id)

    def delete_transaction(self, transaction_id: str):
        return self.transaction_repository.delete_transaction(transaction_id)
