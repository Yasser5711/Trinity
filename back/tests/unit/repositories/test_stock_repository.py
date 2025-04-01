
import repositories.stock_repository as stock_repository
from db.models.models import Stock


def test_get_all(db_session, sample_stock):
    stocks = stock_repository.get_all(db_session)
    assert len(stocks) >= 1


def test_get_by_id(db_session, sample_stock):
    stock = stock_repository.get_by_id(db_session, sample_stock.id)
    assert stock is not None


def test_create(db_session, sample_product):
    new_stock = Stock(product_id=sample_product.id, quantity=50)
    created = stock_repository.create(db_session, new_stock)
    assert created.quantity == 50


def test_update(db_session, sample_stock):
    sample_stock.quantity = 77
    updated = stock_repository.update(db_session, sample_stock)
    assert updated.quantity == 77


def test_delete(db_session, sample_stock):
    stock_repository.delete(db_session, sample_stock)
    result = stock_repository.get_by_id(db_session, sample_stock.id)
    assert result is None
