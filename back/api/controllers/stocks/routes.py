from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.helpers import get_db, has_role
from db.schemas.stock_schemas import StockCreate, StockResponse, StockUpdate
from services import stock_service

router = APIRouter()


@router.get("/stocks", response_model=list[StockResponse], tags=["stocks"])
def get_stocks(db: Session = Depends(get_db), current_user=Depends(has_role("admin"))):
    return stock_service.get_all_stocks(db)


@router.get("/stocks/{stock_id}", response_model=StockResponse, tags=["stocks"])
def get_stock_by_id(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        return stock_service.get_stock_by_id(db, stock_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/stocks", status_code=status.HTTP_201_CREATED, tags=["stocks"])
def create_stock(
    stock: StockCreate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    return stock_service.create_stock(db, stock)


@router.put("/stocks/{stock_id}", tags=["stocks"])
def update_stock(
    stock_id: int,
    stock: StockUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        stock_service.update_stock(db, stock_id, stock)
        return {"message": "Stock updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/stocks/{stock_id}", tags=["stocks"])
def delete_stock(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        stock_service.delete_stock(db, stock_id)
        return {"message": "Stock deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
