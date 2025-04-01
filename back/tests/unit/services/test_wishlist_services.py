import services.wishlist_service as wishlist_service
from db.schemas.wishlist_schemas import WishlistAddItem
import pytest


def test_create_and_get_wishlist_service(db_session, sample_user):
    wishlist = wishlist_service.get_or_create_wishlist(
        db_session, sample_user.id)
    assert wishlist.user_id == sample_user.id


def test_add_to_wishlist_service(db_session, sample_user, sample_product):
    from db.models.models import WishListItem
    data = WishlistAddItem(product_id=sample_product.id)
    wishlist = wishlist_service.add_to_wishlist(
        db_session, sample_user.id, data)
    assert any(isinstance(item, WishListItem) for item in wishlist.items)


def test_add_duplicate_wishlist_item_raises(db_session, sample_user, sample_product):
    data = WishlistAddItem(product_id=sample_product.id)
    wishlist_service.add_to_wishlist(db_session, sample_user.id, data)

    with pytest.raises(ValueError, match="Product already in wishlist"):
        wishlist_service.add_to_wishlist(db_session, sample_user.id, data)


def test_remove_from_wishlist_service(db_session, sample_user, sample_product):
    data = WishlistAddItem(product_id=sample_product.id)
    wishlist_service.add_to_wishlist(db_session, sample_user.id, data)

    wishlist_service.remove_from_wishlist(
        db_session, sample_user.id, sample_product.id)
    # TODO: if it doesn't raise, it's considered successful


def test_delete_wishlist_service(db_session, sample_user, sample_product):
    wishlist_service.add_to_wishlist(
        db_session, sample_user.id, WishlistAddItem(product_id=sample_product.id))
    wishlist_service.delete_wishlist(db_session, sample_user.id)

    with pytest.raises(ValueError, match="Wishlist not found"):
        wishlist_service.delete_wishlist(db_session, sample_user.id)
