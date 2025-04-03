from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.helpers import has_role
from db.models.models import User
from db.schemas.product_schemas import (
    ProductCreate,
    ProductPaginated,
    ProductResponse,
    ProductUpdate,
)
from db.session import get_db
from services import product_service

router = APIRouter()


@router.get("/products", response_model=ProductPaginated, tags=["products"])
def get_products(
    db: Session = Depends(get_db),
    name: str = None,
    brand: str = None,
    category_id: int = None,
    price_min: float = None,
    price_max: float = None,
    limit: int = Query(10, ge=1, le=20),
    page: int = Query(1, ge=1),
):
    filters = {
        "name": name,
        "brand": brand,
        "category_id": category_id,
        "price_min": price_min,
        "price_max": price_max,
    }
    return product_service.get_products(db, filters, limit, page)


@router.get("/products/{product_id}", response_model=ProductResponse, tags=["products"])
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get(
    "/products/barcode/{code}", response_model=ProductResponse, tags=["products"]
)
def get_product_by_code(code: str, db: Session = Depends(get_db)):
    product = product_service.get_product_by_barcode(db, code)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post(
    "/products", response_model=ProductResponse, status_code=201, tags=["products"]
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        return product_service.create_product(db, product)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.put("/products/{product_id}", response_model=ProductResponse, tags=["products"])
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        return product_service.update_product(db, product_id, product)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/products/{product_id}", tags=["products"])
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        product_service.delete_product(db, product_id)
        return {"message": "Product deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/top-products", tags=["products"])
def get_top_products(
    db: Session = Depends(get_db),
    top: int = Query(5, ge=1, le=25),
):
    return {"products": product_service.get_top_random_products(db, top)}
