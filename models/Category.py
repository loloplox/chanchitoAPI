import uuid

from sqlmodel import SQLModel, Field, Relationship

from models.Transaction import TypeTransaction


class Category(SQLModel, table=True):
    id: str | None = Field(default_factory=lambda: uuid.uuid4().__str__(), primary_key=True)
    name: str = Field(nullable=False, unique=True)
    type_transaction: TypeTransaction = Field(nullable=False)

    transactions: list["Transaction"] = Relationship(back_populates="category")


class CategoryRequest(SQLModel):
    name: str
    type_transaction: TypeTransaction


class CategoryResponse(SQLModel):
    id: str
    name: str
    type_transaction: TypeTransaction
