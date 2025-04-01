from sqlalchemy.orm import Session
from db.models.models import Cart, CartStatus
from db.schemas.cart_schemas import CartCreate, CartUpdate
from repositories import cart_repository


def get_all_carts(db: Session):
    return cart_repository.get_all_carts(db)


def get_cart_by_id(db: Session, id: int):
    cart = cart_repository.get_by_id(db, id)
    if not cart:
        raise ValueError("Cart not found")
    return cart


def create_cart(db: Session, data: CartCreate):
    if cart_repository.cart_exists(db, data.user_id):
        raise ValueError("Cart already exists")
    new_cart = Cart(user_id=data.user_id, status=CartStatus.PENDING)
    return cart_repository.create(db, new_cart)


def update_cart(db: Session, cart_id: int, data: CartUpdate):
    cart = cart_repository.get_by_id(db, cart_id)
    if not cart:
        raise ValueError("Cart not found")

    # if data.status and data.status not in CartStatus.__members__.values():
    #     raise ValueError("Invalid status")

    for key, value in data.model_dump(exclude_unset=True).items():
        if key == "status" and value:
            value = value.upper()
        setattr(cart, key, value)

    return cart_repository.update(db, cart)


def delete_cart(db: Session, cart_id: int):
    cart = cart_repository.get_by_id(db, cart_id)
    if not cart:
        raise ValueError("Cart not found")
    cart_repository.delete(db, cart)


def get_cart_statuses():
    return [status.value for status in CartStatus]
