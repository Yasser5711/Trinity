from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.helpers import get_db, has_role
from db.schemas.cart_schemas import (
    CartCreate,
    CartDetailResponse,
    CartResponse,
    CartStatusResponse,
    CartUpdate,
)
from services import cart_service

router = APIRouter()


@router.get("/carts/status", response_model=CartStatusResponse, tags=["cart"])
def get_cart_statuses():
    return {"statuses": cart_service.get_cart_statuses()}


@router.get("/carts", response_model=list[CartResponse], tags=["cart"])
def get_carts(db: Session = Depends(get_db), current_user=Depends(has_role("admin"))):
    return cart_service.get_all_carts(db)


@router.get("/carts/{cart_id}", response_model=CartDetailResponse, tags=["cart"])
def get_cart_by_id(
    cart_id: int, db: Session = Depends(get_db), current_user=Depends(has_role("admin"))
):
    try:
        return cart_service.get_cart_by_id(db, cart_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/carts", tags=["cart"], status_code=status.HTTP_201_CREATED)
def create_cart(
    cart: CartCreate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        new_cart = cart_service.create_cart(db, cart)
        return {"message": "Cart created successfully", "cart_id": new_cart.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.put("/carts/{cart_id}", tags=["cart"])
def update_cart(
    cart_id: int,
    cart_update: CartUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        cart_service.update_cart(db, cart_id, cart_update)
        return {"message": "Cart updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/carts/{cart_id}", tags=["cart"])
def delete_cart(
    cart_id: int, db: Session = Depends(get_db), current_user=Depends(has_role("admin"))
):
    try:
        cart_service.delete_cart(db, cart_id)
        return {"message": "Cart deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
