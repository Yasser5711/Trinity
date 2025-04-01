from sqlalchemy.orm import Session, joinedload
from db.models.models import Cart, CartItem, Product, Invoice, InvoiceItem, Stock


def get_cart_by_user(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).first()


def create_cart(db: Session, user_id: int):
    cart = Cart(user_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_stock(db: Session, product_id: int):
    return db.query(Stock).filter(Stock.product_id == product_id).first()


def get_cart_item(db: Session, item_id: int):
    return db.query(CartItem).filter(CartItem.id == item_id).first()


def add_cart_item(db: Session, item: CartItem):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_cart_item(db: Session, item: CartItem):
    db.delete(item)
    db.commit()


def create_invoice(db: Session, invoice: Invoice):
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


def add_invoice_item(db: Session, item: InvoiceItem):
    db.add(item)


def delete_all_cart_items(db: Session, cart_id: int):
    db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
    db.commit()


def get_user_invoices(db: Session, user_id: int):
    return db.query(Invoice).filter(
        Invoice.user_id == user_id
    ).options(
        joinedload(Invoice.items).joinedload(InvoiceItem.product)
    ).all()


def get_invoice_by_id(db: Session, invoice_id: int, user_id: int):
    return db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == user_id
    ).options(
        joinedload(Invoice.items).joinedload(InvoiceItem.product)
    ).first()
