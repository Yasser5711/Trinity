from datetime import datetime

import pytest

import services.invoice_service as invoice_service
from db.schemas.invoices_schemas import InvoiceCreate, InvoiceUpdate


def test_create_invoice_service(db_session, sample_user, sample_product):
    data = InvoiceCreate(
        user_id=sample_user.id,
        items=[{"product_id": sample_product.id, "quantity": 2, "price": 20.0}],
    )
    invoice = invoice_service.create_invoice(db_session, data)
    assert invoice.total_amount == 40.0


def test_get_invoice_by_id_service(db_session, sample_user, sample_product):
    invoice = invoice_service.create_invoice(
        db_session,
        InvoiceCreate(
            user_id=sample_user.id,
            items=[{"product_id": sample_product.id, "quantity": 1, "price": 10.0}],
        ),
    )
    found = invoice_service.get_invoice_by_id(db_session, invoice.id)
    assert found.id == invoice.id


def test_update_invoice_service(db_session, sample_user, sample_product):
    invoice = invoice_service.create_invoice(
        db_session,
        InvoiceCreate(
            user_id=sample_user.id,
            items=[{"product_id": sample_product.id, "quantity": 1, "price": 10.0}],
        ),
    )
    update_data = InvoiceUpdate(
        items=[{"product_id": sample_product.id, "quantity": 3, "price": 5.0}]
    )
    updated = invoice_service.update_invoice(db_session, invoice.id, update_data)
    assert updated.total_amount == 15.0


def test_delete_invoice_service(db_session, sample_user, sample_product):
    invoice = invoice_service.create_invoice(
        db_session,
        InvoiceCreate(
            user_id=sample_user.id,
            items=[{"product_id": sample_product.id, "quantity": 1, "price": 5.0}],
        ),
    )
    invoice_service.delete_invoice(db_session, invoice.id)
    with pytest.raises(ValueError):
        invoice_service.get_invoice_by_id(db_session, invoice.id)


def test_yearly_sales_service(db_session):
    year = datetime.now().year
    result = invoice_service.get_yearly_sales(db_session, year)
    assert isinstance(result, list)
    assert len(result) == 12


def test_monthly_sales_service(db_session):
    now = datetime.now()
    result = invoice_service.get_monthly_sales(db_session, now.year, now.month)
    assert isinstance(result, dict)
    assert "total_sales" in result
