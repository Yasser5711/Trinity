import pytest
from db.schemas.cart_items_schemas import CartItemCreate, CartItemUpdate
import services.cart_item_service as cart_item_service


def test_list_cart_items(db_session, sample_cart_item):
    items = cart_item_service.list_cart_items(db_session)
    assert any(item.id == sample_cart_item.id for item in items)


def test_get_cart_item_success(db_session, sample_cart_item):
    item = cart_item_service.get_cart_item(db_session, sample_cart_item.id)
    assert item.id == sample_cart_item.id


def test_get_cart_item_not_found(db_session):
    with pytest.raises(ValueError, match="Cart item not found"):
        cart_item_service.get_cart_item(db_session, 9999)


def test_create_cart_item_success(db_session, sample_cart, sample_product):
    data = CartItemCreate(
        cart_id=sample_cart.id,
        product_id=sample_product.id,
        quantity=2
    )

    new_item = cart_item_service.create_cart_item(db_session, data)

    assert new_item.id is not None
    assert new_item.cart_id == sample_cart.id
    assert new_item.product_id == sample_product.id
    assert new_item.quantity == 2
    assert new_item.price == 20.0  # assuming price=10.0


def test_create_cart_item_invalid_product(db_session, sample_cart):
    data = CartItemCreate(
        cart_id=sample_cart.id,
        product_id=9999,
        quantity=1
    )

    with pytest.raises(ValueError, match="Product not found"):
        cart_item_service.create_cart_item(db_session, data)


def test_update_cart_item_success(db_session, sample_cart_item):
    update_data = CartItemUpdate(quantity=4)
    updated = cart_item_service.update_cart_item(
        db_session, sample_cart_item.id, update_data)

    assert updated.quantity == 4
    assert updated.price == 40.0


def test_update_cart_item_not_found(db_session):
    update_data = CartItemUpdate(quantity=2)

    with pytest.raises(ValueError, match="Cart item not found"):
        cart_item_service.update_cart_item(db_session, 9999, update_data)


def test_delete_cart_item_success(db_session, sample_cart_item):
    cart_item_service.delete_cart_item(db_session, sample_cart_item.id)

    with pytest.raises(ValueError):
        cart_item_service.get_cart_item(db_session, sample_cart_item.id)


def test_delete_cart_item_not_found(db_session):
    with pytest.raises(ValueError, match="Cart item not found"):
        cart_item_service.delete_cart_item(db_session, 9999)
