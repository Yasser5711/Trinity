from sqlalchemy.orm import Session

from db.models.models import Stock
from db.schemas.stock_schemas import StockCreate, StockUpdate
from repositories import stock_repository


def get_all_stocks(db: Session):
    return stock_repository.get_all(db)


def get_stock_by_id(db: Session, stock_id: int):
    stock = stock_repository.get_by_id(db, stock_id)
    if not stock:
        raise ValueError("Stock not found")
    return stock


def create_stock(db: Session, data: StockCreate):
    stock = Stock(**data.model_dump())
    return stock_repository.create(db, stock)


def update_stock(db: Session, stock_id: int, data: StockUpdate):
    stock = stock_repository.get_by_id(db, stock_id)
    if not stock:
        raise ValueError("Stock not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(stock, key, value)

    return stock_repository.update(db, stock)


def delete_stock(db: Session, stock_id: int):
    stock = stock_repository.get_by_id(db, stock_id)
    if not stock:
        raise ValueError("Stock not found")

    stock_repository.delete(db, stock)
