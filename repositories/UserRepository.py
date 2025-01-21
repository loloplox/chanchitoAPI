from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlmodel import select

from db.session import get_session
from models.User import UserRequest, User


class UserRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_users(self) -> list[User]:
        all_users = self.session.execute(select(User)).all()
        return [User(**user[0].model_dump()) for user in all_users]

    def get_user_by_username(self, username: str) -> User | bool:
        user_found = self.session.execute(select(User).where(User.username == username)).first()

        if not user_found:
            return False
        return user_found[0]

    def get_user_by_id(self, user_id: str) -> bool | User:
        print(user_id)
        user_found = self.session.get(User, user_id)

        if not user_found:
            return False
        return User(**user_found.model_dump())

    def create_user(self, user: UserRequest):
        try:
            db_user = User.model_validate(user)
            self.session.add(db_user)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
