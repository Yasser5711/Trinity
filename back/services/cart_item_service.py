from sqlalchemy.orm import Session
from db.models.models import CartItem
from db.schemas.cart_items_schemas import CartItemCreate, CartItemUpdate
from repositories import cart_item_repository


def list_cart_items(db: Session):
    return cart_item_repository.get_all(db)


def get_cart_item(db: Session, item_id: int):
    item = cart_item_repository.get_by_id(db, item_id)
    if not item:
        raise ValueError("Cart item not found")
    return item


def create_cart_item(db: Session, data: CartItemCreate):
    product = cart_item_repository.get_product_by_id(db, data.product_id)
    if not product:
        raise ValueError("Product not found")

    item = CartItem(
        cart_id=data.cart_id,
        product_id=data.product_id,
        quantity=data.quantity
    )
    return cart_item_repository.create(db, item)


def update_cart_item(db: Session, item_id: int, data: CartItemUpdate):
    item = cart_item_repository.get_by_id(db, item_id)
    if not item:
        raise ValueError("Cart item not found")

    if data.quantity is not None:
        item.quantity = data.quantity

    return cart_item_repository.update(db, item)


def delete_cart_item(db: Session, item_id: int):
    item = cart_item_repository.get_by_id(db, item_id)
    if not item:
        raise ValueError("Cart item not found")

    cart_item_repository.delete(db, item)
