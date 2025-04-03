import pytest

import services.invoice_item_service as invoice_item_service
from db.schemas.invoice_items_schemas import InvoiceItemCreate, InvoiceItemUpdate


def test_create_invoice_item_service(db_session, sample_product, sample_user):
    from db.models.models import Invoice

    invoice = Invoice(user_id=sample_user.id, total_amount=0.0)
    db_session.add(invoice)
    db_session.commit()

    data = InvoiceItemCreate(
        invoice_id=invoice.id, product_id=sample_product.id, quantity=2, unit_price=50.0
    )
    item = invoice_item_service.create_item(db_session, data)
    assert item.invoice_id == invoice.id
    assert item.quantity == 2


def test_get_item_by_id_service(db_session, sample_product, sample_user):
    from db.models.models import Invoice, InvoiceItem

    invoice = Invoice(user_id=sample_user.id, total_amount=0.0)
    db_session.add(invoice)
    db_session.commit()

    item = InvoiceItem(
        invoice_id=invoice.id, product_id=sample_product.id, quantity=1, unit_price=10.0
    )
    db_session.add(item)
    db_session.commit()

    result = invoice_item_service.get_item_by_id(db_session, item.id)
    assert result.id == item.id


def test_update_invoice_item_service(db_session, sample_product, sample_user):
    from db.models.models import Invoice, InvoiceItem

    invoice = Invoice(user_id=sample_user.id, total_amount=0.0)
    db_session.add(invoice)
    db_session.commit()

    item = InvoiceItem(
        invoice_id=invoice.id, product_id=sample_product.id, quantity=1, unit_price=10.0
    )
    db_session.add(item)
    db_session.commit()

    updated = invoice_item_service.update_item(
        db_session, item.id, InvoiceItemUpdate(quantity=4)
    )
    assert updated.quantity == 4


def test_delete_invoice_item_service(db_session, sample_product, sample_user):
    from db.models.models import Invoice, InvoiceItem

    invoice = Invoice(user_id=sample_user.id, total_amount=0.0)
    db_session.add(invoice)
    db_session.commit()

    item = InvoiceItem(
        invoice_id=invoice.id, product_id=sample_product.id, quantity=1, unit_price=10.0
    )
    db_session.add(item)
    db_session.commit()

    invoice_item_service.delete_item(db_session, item.id)

    with pytest.raises(ValueError):
        invoice_item_service.get_item_by_id(db_session, item.id)
