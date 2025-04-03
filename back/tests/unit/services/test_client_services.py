import repositories.client_cart_repository as client_cart_repository
import services.client_cart_service as client_cart_service
from db.schemas.cart_items_schemas import CartItemCreate, CartItemUpdate


def test_get_or_create_cart(db_session, sample_user):
    cart = client_cart_service.get_or_create_cart(db_session, sample_user.id)
    assert cart.user_id == sample_user.id


def test_add_item_to_cart(db_session, sample_user, sample_product):
    data = CartItemCreate(cart_id=1, product_id=sample_product.id, quantity=1)
    item = client_cart_service.add_item_to_cart(db_session, sample_user.id, data)
    assert item.product_id == sample_product.id


def test_update_cart_item(db_session, sample_cart_item):
    data = CartItemUpdate(quantity=3)
    updated = client_cart_service.update_cart_item(
        db_session, sample_cart_item.id, data
    )
    assert updated.quantity == 3


def test_remove_cart_item(db_session, sample_cart_item):
    client_cart_service.remove_cart_item(db_session, sample_cart_item.id)
    item = client_cart_repository.get_cart_item(db_session, sample_cart_item.id)
    assert item is None


def test_checkout(db_session, sample_user, sample_cart_item):
    invoice = client_cart_service.checkout(db_session, sample_user.id)
    assert invoice.total_amount > 0


def test_get_invoices(db_session, sample_user):
    invoices = client_cart_service.get_invoices(db_session, sample_user.id)
    assert isinstance(invoices, list)


def test_get_invoice(db_session, sample_user, sample_cart_item):
    invoice = client_cart_service.checkout(db_session, sample_user.id)
    result = client_cart_service.get_invoice(db_session, invoice.id, sample_user.id)
    assert result.id == invoice.id
