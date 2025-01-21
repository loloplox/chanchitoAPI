import uuid

from sqlmodel import SQLModel, Field, Relationship

from models.Transaction import Transaction


class User(SQLModel, table=True):
    id: str | None = Field(default=lambda: uuid.uuid4().__str__(), primary_key=True)
    username: str = Field(max_length=100, unique=True)
    password: str = Field()
    active: bool = Field(default=True)
    transactions: list[Transaction | None] = Relationship(back_populates="user")


class UserRequest(SQLModel):
    id: str | None = Field(default=None)
    username: str = Field(max_length=100)
    password: str = Field()


class UserResponse(SQLModel):
    id: str = Field()
    username: str = Field(max_length=100)
    active: bool = Field()
