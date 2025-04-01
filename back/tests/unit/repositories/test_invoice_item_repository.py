import repositories.invoice_item_repository as invoice_item_repository
from tests.factories.product_factory import ProductFactory


def test_create_invoice_item_repo(db_session):
    from db.models.models import InvoiceItem, Invoice
    product = ProductFactory()
    invoice = Invoice(user_id=1, total_amount=0)
    db_session.add(invoice)
    db_session.commit()

    item = InvoiceItem(invoice_id=invoice.id,
                       product_id=product.id, quantity=1, unit_price=10)
    result = invoice_item_repository.create(db_session, item)
    assert result.id


def test_get_invoice_item_by_id_repo(db_session):
    from db.models.models import InvoiceItem, Invoice, Product
    product = ProductFactory()
    invoice = Invoice(user_id=1, total_amount=0)
    db_session.add(invoice)
    db_session.commit()

    item = InvoiceItem(invoice_id=invoice.id,
                       product_id=product.id, quantity=2, unit_price=20)
    db_session.add(item)
    db_session.commit()

    result = invoice_item_repository.get_by_id(db_session, item.id)
    assert result.id == item.id


def test_update_invoice_item_repo(db_session):
    from db.models.models import InvoiceItem, Invoice, Product
    product = ProductFactory()
    invoice = Invoice(user_id=1, total_amount=0)
    db_session.add(invoice)
    db_session.commit()

    item = InvoiceItem(invoice_id=invoice.id,
                       product_id=product.id, quantity=1, unit_price=5)
    db_session.add(item)
    db_session.commit()

    item.quantity = 10
    updated = invoice_item_repository.update(db_session, item)
    assert updated.quantity == 10


def test_delete_invoice_item_repo(db_session):
    from db.models.models import InvoiceItem, Invoice, Product
    product = ProductFactory()
    invoice = Invoice(user_id=1, total_amount=0)
    db_session.add(invoice)
    db_session.commit()

    item = InvoiceItem(invoice_id=invoice.id,
                       product_id=product.id, quantity=1, unit_price=5)
    db_session.add(item)
    db_session.commit()

    invoice_item_repository.delete(db_session, item)
    assert invoice_item_repository.get_by_id(db_session, item.id) is None
