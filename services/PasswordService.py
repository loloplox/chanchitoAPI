from passlib.context import CryptContext


class PasswordService:
    _pwd_context: CryptContext

    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self._pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self._pwd_context.hash(password)
