from sqlalchemy.orm import Session

from db.models.models import Cart, CartItem, Role, User


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()


def get_role_by_id(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def get_cart_by_user_id(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).first()


def delete_cart_and_items(db: Session, cart: Cart):
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.delete(cart)
    db.commit()
