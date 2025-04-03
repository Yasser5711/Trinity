from sqlalchemy.orm import Session

from db.models.models import Cart


def get_all_carts(db: Session):
    return db.query(Cart).all()


def get_by_id(db: Session, cart_id: int):
    return db.query(Cart).filter(Cart.id == cart_id).first()


def get_by_user_id(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).first()


def cart_exists(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).first() is not None


def create(db: Session, cart: Cart):
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def update(db: Session, cart: Cart):
    db.commit()
    db.refresh(cart)
    return cart


def delete(db: Session, cart: Cart):
    if cart.items:
        for item in cart.items:
            db.delete(item)
    db.delete(cart)
    db.commit()
