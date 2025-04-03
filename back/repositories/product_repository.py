from sqlalchemy import func
from sqlalchemy.orm import Session

from db.models.models import Product


def get_products_query(db: Session):
    return db.query(Product)


def get_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_by_barcode(db: Session, barcode: str):
    return db.query(Product).filter(Product.barCode == barcode).first()


def count(db: Session, query):
    return query.count()


def get_paginated(query, offset: int, limit: int):
    return query.offset(offset).limit(limit).all()


def create(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete(db: Session, product: Product):
    if product.stock:
        db.delete(product.stock)
    db.delete(product)
    db.commit()


def get_random_products(db: Session, offset: int, limit: int):
    return db.query(Product).offset(offset).limit(limit).all()


def total_count(db: Session):
    return db.query(func.count(Product.id)).scalar()
