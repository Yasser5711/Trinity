import repositories.client_cart_repository as client_cart_repository
import services.client_cart_service as client_cart_service
from db.models.models import Invoice, CartItem, Stock
from tests.factories.product_factory import ProductFactory


def test_create_and_get_cart(db_session, sample_user):
    cart = client_cart_repository.create_cart(db_session, sample_user.id)
    fetched = client_cart_repository.get_cart_by_user(
        db_session, sample_user.id)
    assert fetched.id == cart.id


def test_get_product(db_session, sample_product):

    product = client_cart_repository.get_product(db_session, sample_product.id)
    assert product.id == sample_product.id


def test_get_stock(db_session, sample_product):
    stock = Stock(product_id=sample_product.id, quantity=10)
    db_session.add(stock)
    db_session.commit()
    db_session.refresh(stock)
    stock = client_cart_repository.get_stock(db_session, sample_product.id)
    print(stock)
    assert stock is not None


def test_add_and_delete_cart_item(db_session, sample_cart):
    product = ProductFactory()
    item = CartItem(cart_id=sample_cart.id, product_id=product.id, quantity=2)
    saved = client_cart_repository.add_cart_item(db_session, item)
    assert saved.id

    client_cart_repository.delete_cart_item(db_session, saved)
    assert client_cart_repository.get_cart_item(db_session, saved.id) is None


def test_create_invoice(db_session, sample_user):
    invoice = Invoice(user_id=sample_user.id, total_amount=0.0)
    saved = client_cart_repository.create_invoice(db_session, invoice)
    assert saved.id


def test_get_user_invoices(db_session, sample_user, sample_cart_item):
    client_cart_service.checkout(db_session, sample_user.id)
    invoices = client_cart_repository.get_user_invoices(
        db_session, sample_user.id)
    assert len(invoices) > 0


def test_get_invoice_by_id(db_session, sample_user, sample_cart_item):
    invoice = client_cart_service.checkout(db_session, sample_user.id)
    fetched = client_cart_repository.get_invoice_by_id(
        db_session, invoice.id, sample_user.id)
    assert fetched.id == invoice.id
