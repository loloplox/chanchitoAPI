import datetime
import uuid
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship


class TypeTransaction(Enum):
    TYPE_BILL = 1
    TYPE_SAVING = 2


class Transaction(SQLModel, table=True):
    id: str | None = Field(default_factory=lambda: uuid.uuid4().__str__(), primary_key=True)
    amount: float = Field(nullable=False)
    type_transaction: TypeTransaction = Field(nullable=False)
    user_id: str = Field(foreign_key="user.id")
    category_id: str = Field(foreign_key="category.id", nullable=False)
    create_date: str = Field(nullable=False, default_factory=lambda: datetime.datetime.now())

    user: "User" = Relationship(back_populates="transactions")
    category: "Category" = Relationship(back_populates="transactions")


class TransactionRequest(SQLModel):
    amount: float = Field(nullable=False)
    type_transaction: TypeTransaction = Field(nullable=False)
    category_id: str = Field(nullable=False)


class TransactionUpdateRequest(SQLModel):
    amount: float | None = Field(nullable=True, default=None)
    type_transaction: TypeTransaction | None = Field(nullable=True, default=None)
    category_id: str | None = Field(nullable=True, default=None)


class TransactionResponse(SQLModel):
    id: str = Field(nullable=False)
    amount: float = Field(nullable=False)
    type_transaction: TypeTransaction = Field(nullable=False)
    category_id: str = Field(nullable=False)
    create_date: str = Field(nullable=False)
