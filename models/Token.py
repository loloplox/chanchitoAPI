from sqlmodel import SQLModel, Field


class Token(SQLModel):
    access_token: str = Field()
    token_type: str = Field(default="bearer")
    username: str = Field()
    user_id: str = Field()


class TokenRequest(SQLModel):
    access_token: str = Field()
