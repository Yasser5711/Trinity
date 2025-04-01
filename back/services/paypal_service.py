from sqlalchemy.orm import Session
from db.models.models import Cart, Invoice, InvoiceItem, Product, Stock, CartItem
from external import paypal_client


def create_paypal_order(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart or not cart.items or cart.status in ["completed", "cancelled"]:
        raise ValueError("Cart is empty or already processed")

    total = 0.0
    items = []
    for item in cart.items:
        product = db.query(Product).filter(
            Product.id == item.product_id).first()
        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        subtotal = item.quantity * product.price
        total += subtotal
        items.append({
            "name": product.name,
            "id": str(product.id),
            "unit_amount": {"currency_code": "USD", "value": f"{product.price:.2f}"},
            "quantity": str(item.quantity)
        })

    access_token = paypal_client.get_paypal_token()

    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": f"{total:.2f}",
                "breakdown": {
                    "item_total": {"currency_code": "USD", "value": f"{total:.2f}"}
                }
            },
            "items": items
        }],
        "application_context": {
            "return_url": "http://localhost:3000/success",
            "cancel_url": "http://localhost:3000/cancel"
        }
    }

    return paypal_client.create_order(access_token, order_data)


def capture_paypal_order(db: Session, user_id: int, order_id: str):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart or not cart.items:
        raise ValueError("Cart is empty or already processed")

    access_token = paypal_client.get_paypal_token()
    order = paypal_client.capture_order(access_token, order_id)

    if order["status"] != "COMPLETED":
        raise ValueError("Order capture failed")

    invoice = Invoice(
        user_id=user_id,
        total_amount=0.0,
        payment_status="Paid",
        paypal_order_id=order_id,
        paypal_capture_id=order["id"]
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    total = 0.0
    for item in cart.items:
        product = db.query(Product).filter(
            Product.id == item.product_id).first()
        stock = db.query(Stock).filter(
            Stock.product_id == item.product_id).first()
        if not product or not stock:
            raise ValueError(
                f"Product or stock not found for item {item.product_id}")
        stock.quantity = max(0, stock.quantity - item.quantity)
        db.commit()

        invoice_item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price
        )
        db.add(invoice_item)
        total += item.quantity * product.price

    invoice.total_amount = total
    db.commit()

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()

    return {
        "message": "Order successfully captured and processed",
        "invoice_id": invoice.id,
        "total_amount": total,
    }
