from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from db.models.models import Category, Product


def get_all_categories(db: Session):
    query = (
        db.query(
            Category.id, Category.name, func.count(Product.id).label("product_count")
        )
        .outerjoin(Product)
        .group_by(Category.id)
        .order_by(func.count(Product.id).desc())
    )
    return query.all()


def get_top_categories(db: Session, top: int):
    return get_all_categories(db).limit(top)


def get_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()


def create(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update(db: Session, category: Category, name: str):
    category.name = name
    db.commit()
    db.refresh(category)
    return category


def delete(db: Session, category: Category):
    db.delete(category)
    db.commit()
