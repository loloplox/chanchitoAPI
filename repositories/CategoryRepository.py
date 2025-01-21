from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlmodel import select

from db.session import get_session
from models.Category import Category, CategoryResponse
from models.Transaction import Transaction, TypeTransaction


class CategoryRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_all_categories(self) -> list[CategoryResponse]:
        categories = self.session.execute(select(Category)).scalars().all()

        return [CategoryResponse(**category.model_dump()) for category in categories]

    def get_all_categories_by_type_transaction(self, type_transaction: int) -> list[CategoryResponse]:
        categories = self.session.execute(
            select(Category).where(Category.type_transaction == type_transaction)).scalars().all()

        return [CategoryResponse(**category.model_dump()) for category in categories]

    def get_category_by_id(self, category_id: int) -> CategoryResponse:
        category = self.session.get(Category, category_id)

        return CategoryResponse(**category.model_dump())
