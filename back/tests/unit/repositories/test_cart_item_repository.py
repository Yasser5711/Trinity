import repositories.cart_item_repository as cart_item_repository
from db.models.models import CartItem


def test_get_all_cart_items(db_session, sample_cart_item):
    items = cart_item_repository.get_all(db_session)
    assert any(item.id == sample_cart_item.id for item in items)


def test_get_by_id_found(db_session, sample_cart_item):
    item = cart_item_repository.get_by_id(db_session, sample_cart_item.id)
    assert isinstance(item, CartItem)
    assert item.id == sample_cart_item.id


def test_get_by_id_not_found(db_session):
    assert cart_item_repository.get_by_id(db_session, 9999) is None


def test_create_cart_item(db_session, sample_cart, sample_product):
    item = CartItem(cart_id=sample_cart.id,
                    product_id=sample_product.id, quantity=1)
    created = cart_item_repository.create(db_session, item)

    assert created.id is not None
    assert created.cart_id == sample_cart.id
    assert created.product_id == sample_product.id
    assert created.quantity == 1


def test_update_cart_item(db_session, sample_cart_item):
    sample_cart_item.quantity = 10
    updated = cart_item_repository.update(db_session, sample_cart_item)

    assert updated.quantity == 10
    assert updated.price == 100.0


def test_delete_cart_item(db_session, sample_cart_item):
    cart_item_repository.delete(db_session, sample_cart_item)
    assert cart_item_repository.get_by_id(
        db_session, sample_cart_item.id) is None


def test_get_product_by_id_found(db_session, sample_product):
    product = cart_item_repository.get_product_by_id(
        db_session, sample_product.id)
    assert product.id == sample_product.id


def test_get_product_by_id_not_found(db_session):
    product = cart_item_repository.get_product_by_id(db_session, 9999)
    assert product is None
