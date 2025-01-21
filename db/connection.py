from decouple import config
from sqlalchemy import create_engine
from sqlmodel import SQLModel
from models import Category, Transaction, User

SQL_USER = config("SQL_USER")
SQL_PASSWORD = config("SQL_PASSWORD")
SQL_HOST = config("SQL_HOST")
SQL_PORT = config("SQL_PORT")
SQL_DATABASE = config("SQL_DATABASE")

SQL_URL = f"postgresql+psycopg2://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}"

engine = create_engine(SQL_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def drop_db():
    SQLModel.metadata.drop_all(engine)
