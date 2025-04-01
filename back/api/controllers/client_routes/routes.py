from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.helpers import login_required
from db.schemas.cart_items_schemas import CartItemCreate, CartItemUpdate
from db.schemas.cart_schemas import CartDetailResponse, CartItemResponse
from db.schemas.invoices_schemas import InvoiceResponse_2, InvoiceResponse
from db.models.models import User
from db.session import get_db
from services import client_cart_service

router = APIRouter()


@router.get("/cart", response_model=CartDetailResponse, status_code=status.HTTP_200_OK, tags=["client-routes"])
def get_cart(
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    return client_cart_service.get_or_create_cart(db, current_user.id)


@router.post("/cart/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED, tags=["client-routes"])
def add_cart_item(
    item: CartItemCreate,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    try:
        return client_cart_service.add_item_to_cart(db, current_user.id, item)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/cart/items/{item_id}", response_model=CartItemResponse, status_code=status.HTTP_200_OK, tags=["client-routes"])
def update_cart_item(
    item_id: int,
    item: CartItemUpdate,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    try:
        return client_cart_service.update_cart_item(db, item_id, item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/cart/items/{item_id}", status_code=status.HTTP_200_OK, tags=["client-routes"])
def remove_cart_item(
    item_id: int,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    try:
        client_cart_service.remove_cart_item(db, item_id)
        return {"message": "Item removed from cart"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/checkout", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED, tags=["client-routes"])
def checkout(
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    try:
        return client_cart_service.checkout(db, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/invoices", response_model=list[InvoiceResponse_2], status_code=status.HTTP_200_OK, tags=["client-routes"])
def get_invoices(
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    return client_cart_service.get_invoices(db, current_user.id)


@router.get("/invoices/{invoice_id}", response_model=InvoiceResponse_2, status_code=status.HTTP_200_OK, tags=["client-routes"])
def get_invoice(
    invoice_id: int,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    try:
        return client_cart_service.get_invoice(db, invoice_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
