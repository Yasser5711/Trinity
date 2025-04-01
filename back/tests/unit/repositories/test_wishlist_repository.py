import repositories.wishlist_repository as wishlist_repository
from db.models.models import WishListItem


def test_create_and_get_wishlist_repo(db_session, sample_user):
    created = wishlist_repository.create_wishlist(db_session, sample_user.id)
    assert created.user_id == sample_user.id

    fetched = wishlist_repository.get_user_wishlist(db_session, sample_user.id)
    assert fetched.id == created.id


def test_add_and_check_item_repo(db_session, sample_user, sample_product):
    wishlist = wishlist_repository.create_wishlist(db_session, sample_user.id)
    item = wishlist_repository.add_item(
        db_session,
        WishListItem(wishlist_id=wishlist.id, product_id=sample_product.id)
    )
    assert item.product_id == sample_product.id

    found = wishlist_repository.is_in_wishlist(
        db_session, wishlist.id, sample_product.id)
    assert found is not None


def test_remove_item_repo(db_session, sample_user, sample_product):
    wishlist = wishlist_repository.create_wishlist(db_session, sample_user.id)
    wishlist_repository.add_item(db_session, WishListItem(
        wishlist_id=wishlist.id, product_id=sample_product.id))

    wishlist_repository.remove_item(db_session, wishlist.id, sample_product.id)
    assert wishlist_repository.is_in_wishlist(
        db_session, wishlist.id, sample_product.id) is None


def test_delete_wishlist_repo(db_session, sample_user):
    wishlist = wishlist_repository.create_wishlist(db_session, sample_user.id)
    wishlist_repository.delete_wishlist(db_session, wishlist)

    assert wishlist_repository.get_user_wishlist(
        db_session, sample_user.id) is None
