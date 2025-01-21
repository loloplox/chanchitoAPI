from fastapi.params import Depends

from repositories.CategoryRepository import CategoryRepository


class CategoryService:
    def __init__(self, category_repository: CategoryRepository = Depends()):
        self.category_repository = category_repository

    def get_all_categories(self):
        return self.category_repository.get_all_categories()

    def get_all_categories_by_type_transaction(self, type_transaction: int):
        return self.category_repository.get_all_categories_by_type_transaction(type_transaction)

    def get_category_by_id(self, category_id: int):
        return self.category_repository.get_category_by_id(category_id)
