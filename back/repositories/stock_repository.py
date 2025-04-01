from sqlalchemy.orm import Session
from db.models.models import Stock


def get_all(db: Session):
    return db.query(Stock).all()


def get_by_id(db: Session, stock_id: int):
    return db.query(Stock).filter(Stock.id == stock_id).first()


def create(db: Session, stock: Stock):
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


def update(db: Session, stock: Stock):
    db.commit()
    db.refresh(stock)
    return stock


def delete(db: Session, stock: Stock):
    db.delete(stock)
    db.commit()
