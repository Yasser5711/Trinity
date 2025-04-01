from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.helpers import has_role, get_db
from db.schemas.invoice_items_schemas import (
    InvoiceItemCreate,
    InvoiceItemUpdate,
    InvoiceItemResponse,
)
from services import invoice_item_service

router = APIRouter()


@router.get("/invoice-items", response_model=list[InvoiceItemResponse], tags=["invoice-items"])
def get_invoice_items(
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    return invoice_item_service.get_all_items(db)


@router.get("/invoice-items/{id}", response_model=InvoiceItemResponse, tags=["invoice-items"])
def get_invoice_item_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    try:
        return invoice_item_service.get_item_by_id(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/invoice-items", status_code=status.HTTP_201_CREATED, tags=["invoice-items"])
def create_invoice_item(
    item: InvoiceItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    return invoice_item_service.create_item(db, item)


@router.put("/invoice-items/{id}", tags=["invoice-items"])
def update_invoice_item(
    id: int,
    item: InvoiceItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    try:
        invoice_item_service.update_item(db, id, item)
        return {"message": "Invoice item updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/invoice-items/{id}", tags=["invoice-items"])
def delete_invoice_item(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    try:
        invoice_item_service.delete_item(db, id)
        return {"message": "Invoice item deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
