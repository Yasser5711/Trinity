from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.helpers import has_role, get_db
from db.schemas.invoices_schemas import (
    InvoiceCreate, InvoiceUpdate, InvoiceResponse
)
from services import invoice_service

router = APIRouter()


@router.get("/invoices/yearly-sales", tags=["invoices"])
def get_yearly_sales(
    year: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    try:
        return {
            "year": year,
            "monthly_sales": invoice_service.get_yearly_sales(db, year)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/invoices/monthly-sales", tags=["invoices"])
def get_monthly_sales(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    try:
        return invoice_service.get_monthly_sales(db, year, month)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/invoices", response_model=list[InvoiceResponse], tags=["invoices"])
def get_invoices(
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    return invoice_service.get_all_invoices(db)


@router.get("/invoices/{id}", response_model=InvoiceResponse, tags=["invoices"])
def get_invoice_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    try:
        return invoice_service.get_invoice_by_id(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/invoices", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED, tags=["invoices"])
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    return invoice_service.create_invoice(db, invoice)


@router.put("/invoices/{id}", tags=["invoices"])
def update_invoice(
    id: int,
    invoice_update: InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    try:
        invoice_service.update_invoice(db, id, invoice_update)
        return {"message": "Invoice updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/invoices/{id}", tags=["invoices"])
def delete_invoice(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    try:
        invoice_service.delete_invoice(db, id)
        return {"message": "Invoice deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
