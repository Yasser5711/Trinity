from datetime import datetime
from sqlalchemy.orm import Session
from db.models.models import Invoice, InvoiceItem
from db.schemas.invoices_schemas import InvoiceCreate, InvoiceUpdate
from repositories import invoice_repository


def get_all_invoices(db: Session):
    return invoice_repository.get_all(db)


def get_invoice_by_id(db: Session, invoice_id: int):
    invoice = invoice_repository.get_by_id(db, invoice_id)
    if not invoice:
        raise ValueError("Invoice not found")
    return invoice


def create_invoice(db: Session, data: InvoiceCreate):
    invoice = Invoice(user_id=data.user_id, total_amount=0.0)
    invoice = invoice_repository.create_invoice(db, invoice)

    total = 0.0
    for item in data.items:
        invoice_item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.price
        )
        total += item.quantity * item.price
        invoice_repository.add_invoice_item(db, invoice_item)

    invoice.total_amount = total
    db.commit()
    return invoice


def update_invoice(db: Session, invoice_id: int, data: InvoiceUpdate):
    invoice = invoice_repository.get_by_id(db, invoice_id)
    if not invoice:
        raise ValueError("Invoice not found")

    invoice.total_amount = 0.0
    invoice_repository.clear_invoice_items(db, invoice_id)

    for item in data.items:
        invoice_item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.price
        )
        invoice.total_amount += item.quantity * item.price
        invoice_repository.add_invoice_item(db, invoice_item)

    db.commit()
    return invoice


def delete_invoice(db: Session, invoice_id: int):
    invoice = invoice_repository.get_by_id(db, invoice_id)
    if not invoice:
        raise ValueError("Invoice not found")
    invoice_repository.delete_invoice(db, invoice)


def get_yearly_sales(db: Session, year: int):
    current_year = datetime.now().year
    if year < 1900 or year > current_year:
        raise ValueError(f"Year must be between 1900 and {current_year}")

    monthly_totals = invoice_repository.get_yearly_sales(db, year)
    monthly_summary = {month: 0.0 for month in range(1, 13)}

    for record in monthly_totals:
        monthly_summary[int(record.month)] = float(record.total)

    return [
        {"month": datetime(1900, m, 1).strftime("%B"), "total": total}
        for m, total in monthly_summary.items()
    ]


def get_monthly_sales(db: Session, year: int, month: int):
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12")

    current_year = datetime.now().year
    if year < 1900 or year > current_year:
        raise ValueError(f"Year must be between 1900 and {current_year}")

    total = invoice_repository.get_monthly_sales(db, year, month)
    return {
        "year": year,
        "month": datetime(1900, month, 1).strftime("%B"),
        "total_sales": total
    }
