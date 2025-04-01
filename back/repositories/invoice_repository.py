from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from db.models.models import Invoice, InvoiceItem


def get_all(db: Session):
    return db.query(Invoice).all()


def get_by_id(db: Session, id: int):
    return db.query(Invoice).filter(Invoice.id == id).first()


def create_invoice(db: Session, invoice: Invoice):
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


def add_invoice_item(db: Session, item: InvoiceItem):
    db.add(item)
    db.commit()


def clear_invoice_items(db: Session, invoice_id: int):
    db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()
    db.commit()


def delete_invoice(db: Session, invoice: Invoice):
    db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice.id).delete()
    db.delete(invoice)
    db.commit()


def get_yearly_sales(db: Session, year: int):
    return db.query(
        extract('month', Invoice.created_at).label('month'),
        func.coalesce(func.sum(Invoice.total_amount), 0).label('total')
    ).filter(
        extract('year', Invoice.created_at) == year
    ).group_by(
        extract('month', Invoice.created_at)
    ).all()


def get_monthly_sales(db: Session, year: int, month: int):
    return db.query(
        func.coalesce(func.sum(Invoice.total_amount), 0)
    ).filter(
        extract('year', Invoice.created_at) == year,
        extract('month', Invoice.created_at) == month
    ).scalar()
