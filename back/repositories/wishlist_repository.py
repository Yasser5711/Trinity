from sqlalchemy.orm import Session
from db.models.models import WishList, WishListItem, Product


def get_user_wishlist(db: Session, user_id: int):
    return db.query(WishList).filter(WishList.user_id == user_id).first()


def create_wishlist(db: Session, user_id: int):
    wishlist = WishList(user_id=user_id)
    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)
    return wishlist


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def is_in_wishlist(db: Session, wishlist_id: int, product_id: int):
    return db.query(WishListItem).filter(
        WishListItem.wishlist_id == wishlist_id,
        WishListItem.product_id == product_id
    ).first()


def add_item(db: Session, item: WishListItem):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def remove_item(db: Session, wishlist_id: int, product_id: int):
    item = is_in_wishlist(db, wishlist_id, product_id)
    if item:
        db.delete(item)
        db.commit()


def delete_wishlist(db: Session, wishlist: WishList):
    db.delete(wishlist)
    db.commit()
