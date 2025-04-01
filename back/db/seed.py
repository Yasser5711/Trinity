import json
import os
import uuid

from core.helpers.bcrypt import hash_password
from db.models.models import (
    Address,
    Cart,
    CartItem,
    Category,
    Invoice,
    InvoiceItem,
    Product,
    Role,
    Stock,
    User,
    WishList,
)
from db.session import SessionLocal
import random


def init_db():
    db = SessionLocal()
    try:

        addUsersAdmins(db)
        addCategoriesAndProducts(db)
        addUsers(db)
        addAddressToUsers(db)
        addInvoiceAndInvoiceItem(db)
        addCartAndCartItem(db)
        # addWishlist(db)

        db.commit()
        print("Database seeded successfully.")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()


def addUsersAdmins(db):
    admin_role = db.query(Role).filter_by(name="admin").first()
    user_role = db.query(Role).filter_by(name="user").first()

    if not admin_role:
        admin_role = Role(name="admin")
        db.add(admin_role)
    if not user_role:
        user_role = Role(name="user")
        db.add(user_role)

    db.commit()

    admin_user = db.query(User).filter_by(email="admin@admin.com").first()
    if not admin_user:
        hashed_password = hash_password("admin123")
        admin_user = User(
            first_name="Fadmin",
            last_name="Ladmin",
            email="admin@admin.com",
            password=hashed_password,
            roles=[admin_role],
        )
        db.add(admin_user)

    normal_user = db.query(User).filter_by(email="adm@adm.com").first()
    if not normal_user:

        hashed_password = hash_password("adm")
        normal_user = User(
            first_name="adm",
            last_name="adm",
            email="adm@adm.com",
            password=hashed_password,
            roles=[admin_role]

        )
        db.add(normal_user)


def addCategoriesAndProducts(db):

    with open('/app/db/scripts-db/products_V1.json', 'r') as file:
        data = json.load(file)

    for product in data:
        category_id = 0
        print(f"Category: {product['category']}")

        existing_category = db.query(Category).filter(
            Category.name == product['category']).first()
        if existing_category:
            print(
                f"Category '{product['category']}' already exists. Skipping.")
            category_id = existing_category.id
            print(category_id)
        else:
            new_category = Category(name=product['category'])
            db.add(new_category)
            db.commit()
            db.refresh(new_category)
            category_id = new_category.id
            print(f"Category '{product['category']}' added successfully.")
            print(category_id)
        print(f"Category ID for product '{product['name']}': {category_id}")
        existing_product = db.query(Product).filter(
            Product.name == product['name']).first()
        if existing_product:
            print(f"Product '{product['name']}' already exists. Skipping.")
            continue
        new_product = Product(
            name=product['name'],
            barCode=product['barCode'],
            description=product['description'],
            price=product['price'],
            quantity=product["quantity"],
            picture=product['picture'],
            brand=product['brandId'],
            ingredients=product['ingredients'],
            nutriScore=product['nutriScore'],
            nutrition=product['nutrition'],
            allergens=product['allergens'],
            category_id=category_id,

        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        new_stock = Stock(product_id=new_product.id,
                          quantity=random.randint(10, 100))
        db.add(new_stock)
        db.commit()
        db.refresh(new_stock)
        print(f"Product '{product['name']}' added successfully.")


def addUsers(db):
    admin_role = db.query(Role).filter_by(name="admin").first()
    user_role = db.query(Role).filter_by(name="user").first()
    with open('/app/db/scripts-db/users.json', 'r') as file:
        data = json.load(file)

    for user in data:
        hashed_password = hash_password(user["password"])
        normal_user = User(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            password=hashed_password,
            roles=[admin_role],
            phone=user["phone"]
        )
        db.add(normal_user)
        db.commit()
        db.refresh(normal_user)


def addAddressToUsers(db):
    with open('/app/db/scripts-db/addresses.json', 'r') as file:
        data = json.load(file)

    for address in data:
        new_address = Address(
            user_id=address["user_id"],
            address_line=address["address_line"],
            city=address["city"],
            zip_code=address["zip_code"],
            country=address["country"],
        )
        db.add(new_address)
        db.commit()
        db.refresh(new_address)

# def addWishlist(db):
#     with open('/app/db/scripts-db/wishlist.json', 'r') as file:
#         data = json.load(file)

#     for wishlist in data:
#         new_wishlist = WishList(
#             user_id=wishlist["user_id"],
#             product_id=wishlist["product_id"],
#         )
#         db.add(new_wishlist)
#         db.commit()
#         db.refresh(new_wishlist)


def addInvoiceAndInvoiceItem(db):
    with open('/app/db/scripts-db/invoices.json', 'r') as file:
        data = json.load(file)

    for invoice in data:
        new_invoice = Invoice(
            total_amount=invoice["total_amount"],
            user_id=invoice["user_id"],
            payment_status=invoice["payment_status"],
        )
        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)

    with open('/app/db/scripts-db/invoices_item.json', 'r') as file:
        data = json.load(file)

    for invoice_item in data:
        new_invoice_item = InvoiceItem(
            product_id=invoice_item["product_id"],
            quantity=invoice_item["quantity"],
            invoice_id=invoice_item["invoice_id"],
            unit_price=invoice_item["unit_price"],
        )
        db.add(new_invoice_item)
        db.commit()
        db.refresh(new_invoice_item)


def addCartAndCartItem(db):
    with open('/app/db/scripts-db/cart.json', 'r') as file:
        data = json.load(file)

        for cart in data:
            new_cart = Cart(
                user_id=cart["user_id"],

            )
            db.add(new_cart)
            db.commit()
            db.refresh(new_cart)

    with open('/app/db/scripts-db/cart_item.json', 'r') as file:
        data = json.load(file)

        for cart_item in data:
            new_cart_item = CartItem(
                product_id=cart_item["product_id"],
                quantity=cart_item["quantity"],
                cart_id=cart_item["cart_id"],

            )
            db.add(new_cart_item)
            db.commit()
            db.refresh(new_cart_item)


if __name__ == "__main__":
    init_db()
