from sqlalchemy.orm import Session
from db.models.models import WishListItem
from db.schemas.wishlist_schemas import WishlistAddItem
from repositories import wishlist_repository


def get_or_create_wishlist(db: Session, user_id: int):
    wishlist = wishlist_repository.get_user_wishlist(db, user_id)
    if not wishlist:
        wishlist = wishlist_repository.create_wishlist(db, user_id)
    return wishlist


def add_to_wishlist(db: Session, user_id: int, data: WishlistAddItem):
    wishlist = get_or_create_wishlist(db, user_id)

    if wishlist_repository.is_in_wishlist(db, wishlist.id, data.product_id):
        raise ValueError("Product already in wishlist")

    product = wishlist_repository.get_product(db, data.product_id)
    if not product:
        raise ValueError("Product not found")

    item = WishListItem(wishlist_id=wishlist.id, product_id=data.product_id)
    wishlist_repository.add_item(db, item)

    return get_or_create_wishlist(db, user_id)


def remove_from_wishlist(db: Session, user_id: int, product_id: int):
    wishlist = wishlist_repository.get_user_wishlist(db, user_id)
    if not wishlist:
        raise ValueError("Wishlist not found")
    product = wishlist_repository.get_product(db, product_id)
    if not product:
        raise ValueError("Product not found")

    wishlist_repository.remove_item(db, wishlist.id, product_id)


def delete_wishlist(db: Session, user_id: int):
    wishlist = wishlist_repository.get_user_wishlist(db, user_id)
    if not wishlist:
        raise ValueError("Wishlist not found")
    wishlist_repository.delete_wishlist(db, wishlist)
