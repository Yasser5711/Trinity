from sqlalchemy.orm import Session

from db.models.models import Category
from db.schemas.category_schemas import CategoryCreate, CategoryUpdate
from repositories import category_repository


def get_categories(db: Session, top: int = None):
    categories = category_repository.get_all_categories(db)
    if top:
        categories = categories[:top]
    return [
        {"id": c.id, "name": c.name, "product_count": c.product_count}
        for c in categories
    ]


def create_category(db: Session, data: CategoryCreate):
    if category_repository.get_by_name(db, data.name):
        raise ValueError("Category already exists")
    category = Category(name=data.name)
    return category_repository.create(db, category)


def update_category(db: Session, category_id: int, data: CategoryUpdate):
    category = category_repository.get_by_id(db, category_id)
    if not category:
        raise ValueError("Category not found")
    return category_repository.update(db, category, data.name)


def delete_category(db: Session, category_id: int):
    category = category_repository.get_by_id(db, category_id)
    if not category:
        raise ValueError("Category not found")
    category_repository.delete(db, category)
