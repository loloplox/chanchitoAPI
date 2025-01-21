from typing import Type

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlmodel import select

from db.session import get_session
from models.Transaction import Transaction, TransactionRequest, TransactionResponse, TransactionUpdateRequest


class TransactionRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_transactions_by_user_id(self, user_id: str) -> list[Transaction]:
        transactions_found = self.session.execute(
            select(Transaction).where(Transaction.user_id == user_id)).scalars().all()

        if not transactions_found:
            return []
        else:
            return [Transaction(**transaction.model_dump()) for transaction in transactions_found]

    def get_transaction_by_id(self, transaction_id: str) -> Type[Transaction]:
        transaction_found = self.session.get(Transaction, transaction_id)

        if not transaction_found:
            return False
        return transaction_found

    def create_transaction(self, transaction: TransactionRequest, user_id: str) -> TransactionResponse:
        db_transaction = Transaction.model_validate(transaction, update={"user_id": user_id})

        self.session.add(db_transaction)
        self.session.commit()
        self.session.refresh(db_transaction)

        return TransactionResponse(**db_transaction.model_dump())

    def update_transaction(self, transaction: TransactionUpdateRequest, transaction_id: str) -> TransactionResponse:
        transaction_found = self.session.get(Transaction, transaction_id)

        if not transaction_found:
            raise HTTPException(status_code=404, detail="Transaction not found")

        for key, value in transaction.model_dump(exclude_unset=True).items():
            setattr(transaction_found, key, value)

        self.session.commit()
        self.session.refresh(transaction_found)

        return TransactionResponse(**transaction_found.model_dump())

    def delete_transaction(self, transaction_id: str) -> bool:
        transaction_found = self.get_transaction_by_id(transaction_id)
    
        if not transaction_found:
            return False

        self.session.delete(transaction_found)
        self.session.commit()

        return True
