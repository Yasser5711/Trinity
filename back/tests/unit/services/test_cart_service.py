from db.schemas.cart_schemas import CartCreate, CartUpdate
from db.models.models import CartStatus
import services.cart_service as cart_service
import pytest
from pydantic import ValidationError


def test_create_cart_success(db_session, sample_user):
    data = CartCreate(user_id=sample_user.id)
    new_cart = cart_service.create_cart(db_session, data)

    assert new_cart.id is not None
    assert new_cart.user_id == sample_user.id
    assert new_cart.status == CartStatus.PENDING


def test_create_cart_duplicate(db_session, sample_cart):
    data = CartCreate(user_id=sample_cart.user_id)
    with pytest.raises(ValueError, match="Cart already exists"):
        cart_service.create_cart(db_session, data)


def test_get_cart_by_id_success(db_session, sample_cart):
    cart = cart_service.get_cart_by_id(db_session, sample_cart.id)
    assert cart.id == sample_cart.id


def test_get_cart_by_id_not_found(db_session):
    with pytest.raises(ValueError, match="Cart not found"):
        cart_service.get_cart_by_id(db_session, id=9999)


def test_update_cart_status_success(db_session, sample_cart):
    update_data = CartUpdate(status="completed")
    updated = cart_service.update_cart(db_session, sample_cart.id, update_data)
    assert updated.status == CartStatus.COMPLETED


def test_update_cart_invalid_status(db_session, sample_cart):
    with pytest.raises(ValidationError):
        CartUpdate(status="INVALID_STATUS")


def test_delete_cart_success(db_session, sample_cart):
    cart_service.delete_cart(db_session, sample_cart.id)

    with pytest.raises(ValueError, match="Cart not found"):
        cart_service.get_cart_by_id(db_session, sample_cart.id)


def test_get_all_carts(db_session, sample_cart):
    carts = cart_service.get_all_carts(db_session)
    assert isinstance(carts, list)
    assert sample_cart in carts


def test_get_cart_statuses():
    statuses = cart_service.get_cart_statuses()
    assert set(statuses) == {"pending", "completed", "cancelled"}
