from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.helpers import get_db, has_role
from db.schemas.cart_items_schemas import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
)
from services import cart_item_service

router = APIRouter()


@router.get("/cart-items", response_model=list[CartItemResponse], tags=["cart-items"])
def get_cart_items(
    db: Session = Depends(get_db), current_user=Depends(has_role("admin"))
):
    items = cart_item_service.list_cart_items(db)
    return [
        {
            "id": item.id,
            "cart_id": item.cart_id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price,
        }
        for item in items
    ]


@router.get(
    "/cart-items/{cart_item_id}", response_model=CartItemResponse, tags=["cart-items"]
)
def get_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        item = cart_item_service.get_cart_item(db, cart_item_id)
        return {
            "id": item.id,
            "cart_id": item.cart_id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/cart-items", tags=["cart-items"], status_code=status.HTTP_201_CREATED)
def create_cart_item(
    cart_item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        new_item = cart_item_service.create_cart_item(db, cart_item)
        return {
            "message": "Cart item added successfully",
            "cart_item_id": new_item.id,
            "price": new_item.price,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.put("/cart-items/{cart_item_id}", tags=["cart-items"])
def update_cart_item(
    cart_item_id: int,
    cart_item: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        updated_item = cart_item_service.update_cart_item(db, cart_item_id, cart_item)
        return {
            "message": "Cart item updated successfully",
            "price": updated_item.price,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/cart-items/{cart_item_id}", tags=["cart-items"])
def delete_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        cart_item_service.delete_cart_item(db, cart_item_id)
        return {"message": "Cart item deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
