import repositories.invoice_repository as invoice_repository
from db.models.models import Invoice
from datetime import datetime


def test_get_all_invoices(db_session):
    result = invoice_repository.get_all(db_session)
    assert isinstance(result, list)


def test_create_invoice_repo(db_session, sample_user):
    invoice = Invoice(user_id=sample_user.id, total_amount=99.0)
    saved = invoice_repository.create_invoice(db_session, invoice)
    assert saved.id


def test_get_invoice_by_id_repo(db_session, sample_user):
    invoice = Invoice(user_id=sample_user.id, total_amount=5.0)
    db_session.add(invoice)
    db_session.commit()
    result = invoice_repository.get_by_id(db_session, invoice.id)
    assert result.id == invoice.id


def test_delete_invoice_repo(db_session, sample_user):
    invoice = Invoice(user_id=sample_user.id, total_amount=5.0)
    db_session.add(invoice)
    db_session.commit()
    invoice_repository.delete_invoice(db_session, invoice)
    result = invoice_repository.get_by_id(db_session, invoice.id)
    assert result is None


def test_get_yearly_sales_repo(db_session):
    year = datetime.now().year
    result = invoice_repository.get_yearly_sales(db_session, year)
    assert isinstance(result, list)


def test_get_monthly_sales_repo(db_session):
    now = datetime.now()
    total = invoice_repository.get_monthly_sales(
        db_session, now.year, now.month)
    assert isinstance(total, (float, int))
