from sqlalchemy.orm import Session

from db.models.models import CartItem, Invoice, InvoiceItem
from db.schemas.cart_items_schemas import CartItemCreate, CartItemUpdate
from repositories import client_cart_repository


def get_or_create_cart(db: Session, user_id: int):
    cart = client_cart_repository.get_cart_by_user(db, user_id)
    if not cart:
        cart = client_cart_repository.create_cart(db, user_id)
    return cart


def add_item_to_cart(db: Session, user_id: int, data: CartItemCreate):
    product = client_cart_repository.get_product(db, data.product_id)
    if not product:
        raise ValueError("Product not found")

    cart = get_or_create_cart(db, user_id)

    item = CartItem(cart_id=cart.id, product_id=data.product_id, quantity=data.quantity)
    return client_cart_repository.add_cart_item(db, item)


def update_cart_item(db: Session, item_id: int, data: CartItemUpdate):
    item = client_cart_repository.get_cart_item(db, item_id)
    if not item:
        raise ValueError("Cart item not found")

    product = client_cart_repository.get_product(db, item.product_id)
    stock = client_cart_repository.get_stock(db, item.product_id)
    if not product or not stock:
        raise ValueError("Product or stock not found")

    if data.quantity > stock.quantity:
        raise ValueError("Not enough stock")

    item.quantity = data.quantity
    stock.quantity -= data.quantity
    db.commit()
    db.refresh(item)
    db.refresh(stock)

    return item


def remove_cart_item(db: Session, item_id: int):
    item = client_cart_repository.get_cart_item(db, item_id)
    if not item:
        raise ValueError("Cart item not found")
    client_cart_repository.delete_cart_item(db, item)


def checkout(db: Session, user_id: int):
    cart = client_cart_repository.get_cart_by_user(db, user_id)
    if not cart or not cart.items:
        raise ValueError("Cart is empty")

    invoice = Invoice(user_id=user_id, total_amount=0.0)
    invoice = client_cart_repository.create_invoice(db, invoice)

    total = 0.0
    for item in cart.items:
        total += item.quantity * item.product.price

        invoice_item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.product.price,
        )
        client_cart_repository.add_invoice_item(db, invoice_item)

    invoice.total_amount = total
    db.commit()

    client_cart_repository.delete_all_cart_items(db, cart.id)

    return invoice


def get_invoices(db: Session, user_id: int):
    return client_cart_repository.get_user_invoices(db, user_id)


def get_invoice(db: Session, invoice_id: int, user_id: int):
    invoice = client_cart_repository.get_invoice_by_id(db, invoice_id, user_id)
    if not invoice:
        raise ValueError("Invoice not found")
    return invoice
