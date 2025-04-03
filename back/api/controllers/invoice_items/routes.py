from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.helpers import get_db, has_role
from db.schemas.invoice_items_schemas import (
    InvoiceItemCreate,
    InvoiceItemResponse,
    InvoiceItemUpdate,
)
from services import invoice_item_service

router = APIRouter()


@router.get(
    "/invoice-items", response_model=list[InvoiceItemResponse], tags=["invoice-items"]
)
def get_invoice_items(
    db: Session = Depends(get_db), current_user=Depends(has_role("admin"))
):
    return invoice_item_service.get_all_items(db)


@router.get(
    "/invoice-items/{invoice_item_id}",
    response_model=InvoiceItemResponse,
    tags=["invoice-items"],
)
def get_invoice_item_by_id(
    invoice_item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        return invoice_item_service.get_item_by_id(db, invoice_item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post(
    "/invoice-items", status_code=status.HTTP_201_CREATED, tags=["invoice-items"]
)
def create_invoice_item(
    item: InvoiceItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    return invoice_item_service.create_item(db, item)


@router.put("/invoice-items/{invoice_item_id}", tags=["invoice-items"])
def update_invoice_item(
    invoice_item_id: int,
    item: InvoiceItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        invoice_item_service.update_item(db, invoice_item_id, item)
        return {"message": "Invoice item updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/invoice-items/{invoice_item_id}", tags=["invoice-items"])
def delete_invoice_item(
    invoice_item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        invoice_item_service.delete_item(db, invoice_item_id)
        return {"message": "Invoice item deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
