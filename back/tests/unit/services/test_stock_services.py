import pytest
from db.schemas.stock_schemas import StockCreate, StockUpdate
import services.stock_service as stock_service
from db.models.models import Stock


def test_get_all_stocks(db_session, sample_stock):
    stocks = stock_service.get_all_stocks(db_session)
    assert len(stocks) >= 1


def test_get_stock_by_id(db_session, sample_stock):
    stock = stock_service.get_stock_by_id(db_session, sample_stock.id)
    assert stock.id == sample_stock.id


def test_get_stock_by_id_not_found(db_session):
    with pytest.raises(ValueError, match="Stock not found"):
        stock_service.get_stock_by_id(db_session, 9999)


def test_create_stock(db_session, sample_product):
    data = StockCreate(product_id=sample_product.id, quantity=20)
    stock = stock_service.create_stock(db_session, data)
    assert stock.quantity == 20
    assert stock.product_id == sample_product.id


def test_update_stock(db_session, sample_stock):
    data = StockUpdate(quantity=99)
    updated = stock_service.update_stock(db_session, sample_stock.id, data)
    assert updated.quantity == 99


def test_delete_stock(db_session, sample_stock):
    stock_service.delete_stock(db_session, sample_stock.id)
    with pytest.raises(ValueError):
        stock_service.get_stock_by_id(db_session, sample_stock.id)
