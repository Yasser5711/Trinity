import json
import os
import random
import sys

from core.helpers.bcrypt import hash_password
from db.models.models import Category, Product, Role, Stock, User
from db.session import SessionLocal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_PATH = os.path.join(BASE_DIR, "scripts_db", "products_V1.json")
USERS_PATH = os.path.join(BASE_DIR, "scripts_db", "users.json")


def init_db():
    db = SessionLocal()
    try:
        add_roles(db)
        add_admin_users(db)
        add_categories_and_products(db)
        add_bulk_users(db)
        db.commit()
        print("✅ DB seeded successfully.")  # noqa: T201
    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")  # noqa: T201
        sys.exit(1)
    finally:
        db.close()


def add_roles(db):
    for role_name in ["admin", "user"]:
        if not db.query(Role).filter_by(name=role_name).first():
            db.add(Role(name=role_name))
    db.commit()


def add_admin_users(db):
    admin_role = db.query(Role).filter_by(name="admin").first()

    def ensure_user(email, password, first_name, last_name):
        if not db.query(User).filter_by(email=email).first():
            user = User(
                email=email,
                password=hash_password(password),
                first_name=first_name,
                last_name=last_name,
                roles=[admin_role],
            )
            db.add(user)

    ensure_user("admin@admin.com", "admin123", "Fadmin", "Ladmin")
    ensure_user("adm@adm.com", "adm", "adm", "adm")
    db.commit()


def add_categories_and_products(db):
    if not os.path.exists(PRODUCTS_PATH):
        raise FileNotFoundError(f"Product file not found: {PRODUCTS_PATH}")

    with open(PRODUCTS_PATH, encoding="utf-8") as file:
        data = json.load(file)

    for product in data:
        if db.query(Product).filter_by(name=product["name"]).first():
            continue

        category = db.query(Category).filter_by(name=product["category"]).first()
        if not category:
            category = Category(name=product["category"])
            db.add(category)
            db.commit()
            db.refresh(category)

        new_product = Product(
            name=product["name"],
            barCode=product["barCode"],
            description=product["description"],
            price=product["price"],
            quantity=product["quantity"],
            picture=product["picture"],
            brand=product["brandId"],
            ingredients=product["ingredients"],
            nutriScore=product["nutriScore"],
            nutrition=product["nutrition"],
            allergens=product["allergens"],
            category_id=category.id,
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        stock = Stock(product_id=new_product.id, quantity=random.randint(10, 100))  # noqa: S311
        db.add(stock)
        db.commit()


def add_bulk_users(db):
    if not os.path.exists(USERS_PATH):
        raise FileNotFoundError(f"User file not found: {USERS_PATH}")

    with open(USERS_PATH, encoding="utf-8") as file:
        data = json.load(file)

    admin_role = db.query(Role).filter_by(name="admin").first()
    user_role = db.query(Role).filter_by(name="user").first()

    for index, user in enumerate(data):
        if db.query(User).filter_by(email=user["email"]).first():
            continue

        role = admin_role if index % 2 == 0 else user_role
        new_user = User(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            password=hash_password(user["password"]),
            phone=user.get("phone"),
            roles=[role],
        )
        db.add(new_user)
        db.commit()


if __name__ == "__main__":
    init_db()
