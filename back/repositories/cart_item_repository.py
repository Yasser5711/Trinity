from sqlalchemy.orm import Session

from db.models.models import CartItem, Product


def get_all(db: Session):
    return db.query(CartItem).all()


def get_by_id(db: Session, cart_item_id: int):
    return db.query(CartItem).filter(CartItem.id == cart_item_id).first()


def create(db: Session, item: CartItem):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update(db: Session, item: CartItem):
    db.commit()
    db.refresh(item)
    return item


def delete(db: Session, item: CartItem):
    db.delete(item)
    db.commit()


def get_product_by_id(db: Session, cart_item_id: int):
    return db.query(Product).filter(Product.id == cart_item_id).first()
