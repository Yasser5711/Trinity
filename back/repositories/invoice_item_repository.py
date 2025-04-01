from sqlalchemy.orm import Session
from db.models.models import InvoiceItem


def get_all(db: Session):
    return db.query(InvoiceItem).all()


def get_by_id(db: Session, id: int):
    return db.query(InvoiceItem).filter(InvoiceItem.id == id).first()


def create(db: Session, item: InvoiceItem):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update(db: Session, item: InvoiceItem):
    db.commit()
    db.refresh(item)
    return item


def delete(db: Session, item: InvoiceItem):
    db.delete(item)
    db.commit()
