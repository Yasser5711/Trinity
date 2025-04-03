from sqlalchemy.orm import Session

from db.models.models import InvoiceItem
from db.schemas.invoice_items_schemas import InvoiceItemCreate, InvoiceItemUpdate
from repositories import invoice_item_repository


def get_all_items(db: Session):
    return invoice_item_repository.get_all(db)


def get_item_by_id(db: Session, item_id: int):
    item = invoice_item_repository.get_by_id(db, item_id)
    if not item:
        raise ValueError("Invoice item not found")
    return item


def create_item(db: Session, data: InvoiceItemCreate):
    item = InvoiceItem(**data.model_dump())
    return invoice_item_repository.create(db, item)


def update_item(db: Session, item_id: int, data: InvoiceItemUpdate):
    item = invoice_item_repository.get_by_id(db, item_id)
    if not item:
        raise ValueError("Invoice item not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    return invoice_item_repository.update(db, item)


def delete_item(db: Session, item_id: int):
    item = invoice_item_repository.get_by_id(db, item_id)
    if not item:
        raise ValueError("Invoice item not found")

    invoice_item_repository.delete(db, item)
