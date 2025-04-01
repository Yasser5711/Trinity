from sqlalchemy.orm import Session
from db.models.models import Cart, CartStatus
import repositories.cart_repository as cart_repository


def test_create_cart(db_session: Session, sample_user):
    cart = Cart(user_id=sample_user.id, status=CartStatus.PENDING)
    created = cart_repository.create(db_session, cart)

    assert created.id is not None
    assert created.user_id == sample_user.id
    assert created.status == CartStatus.PENDING


def test_get_all_carts(db_session: Session, sample_cart):
    carts = cart_repository.get_all_carts(db_session)
    assert isinstance(carts, list)
    assert sample_cart in carts


def test_get_by_id(db_session: Session, sample_cart):
    cart = cart_repository.get_by_id(db_session, sample_cart.id)
    assert cart is not None
    assert cart.id == sample_cart.id


def test_get_by_user_id(db_session: Session, sample_cart, sample_user):
    cart = cart_repository.get_by_user_id(db_session, sample_user.id)
    assert cart is not None
    assert cart.id == sample_cart.id


def test_cart_exists(db_session: Session, sample_user, sample_cart):
    exists = cart_repository.cart_exists(db_session, sample_user.id)
    assert exists is True


def test_delete_cart(db_session: Session, sample_cart):
    cart_id = sample_cart.id
    cart_repository.delete(db_session, sample_cart)

    deleted = cart_repository.get_by_id(db_session, cart_id)
    assert deleted is None


def test_update_cart(db_session: Session, sample_cart):
    sample_cart.status = CartStatus.COMPLETED
    updated = cart_repository.update(db_session, sample_cart)

    assert updated.status == CartStatus.COMPLETED
