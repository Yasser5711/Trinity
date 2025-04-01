import math
import random
from sqlalchemy.orm import Session
from db.models.models import Product
from db.schemas.product_schemas import ProductCreate, ProductUpdate
from repositories import product_repository
from db.models.models import Category


def filter_products(query, filters: dict):
    if filters.get("name"):
        query = query.filter(Product.name.ilike(f"%{filters['name']}%"))
    if filters.get("brand"):
        query = query.filter(Product.brand.ilike(f"%{filters['brand']}%"))
    if filters.get("category_id"):
        query = query.filter(Product.category_id == filters["category_id"])
    if filters.get("price_min") is not None:
        query = query.filter(Product.price >= filters["price_min"])
    if filters.get("price_max") is not None:
        query = query.filter(Product.price <= filters["price_max"])
    return query


def get_products(db: Session, filters: dict, limit: int, page: int):
    query = product_repository.get_products_query(db)
    query = filter_products(query, filters)
    total = product_repository.count(db, query)

    total_pages = max(math.ceil(total / limit), 1)
    offset = (page - 1) * limit

    if page > total_pages:
        return {
            "total": total,
            "limit": limit,
            "page": page,
            "total_pages": total_pages,
            "products": [],
            "message": f"Page {page} is out of range. Only {total_pages} pages available."
        }

    products = product_repository.get_paginated(query, offset, limit)

    return {
        "total": total,
        "limit": limit,
        "page": page,
        "next_page": page + 1 if page < total_pages else None,
        "prev_page": page - 1 if page > 1 else None,
        "total_pages": total_pages,
        "products": products,
    }


def get_product_by_id(db: Session, product_id: int):
    return product_repository.get_by_id(db, product_id)


def get_product_by_barcode(db: Session, barcode: str):
    return product_repository.get_by_barcode(db, barcode)


def create_product(db: Session, data: ProductCreate):
    if not db.query(Category).filter(Category.id == data.category_id).first():
        raise ValueError("Category not found")
    product = Product(**data.model_dump())
    return product_repository.create(db, product)


def update_product(db: Session, product_id: int, data: ProductUpdate):
    product = product_repository.get_by_id(db, product_id)
    if not product:
        raise ValueError("Product not found")
    if data.category_id:
        category_exists = db.query(Category).filter(
            Category.id == data.category_id).first()
        if not category_exists:
            raise ValueError("Category not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = product_repository.get_by_id(db, product_id)
    if not product:
        raise ValueError("Product not found")
    product_repository.delete(db, product)


def get_top_random_products(db: Session, top: int):
    total = product_repository.total_count(db)
    if total == 0:
        return []

    top = min(top, total)
    offset = random.randint(0, max(0, total - top))
    return product_repository.get_random_products(db, offset, top)
