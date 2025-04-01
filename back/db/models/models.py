import logging
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import declarative_base, relationship

from ..session import SessionLocal, engine

Base = declarative_base()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50), nullable=True)

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password = Column(Text, nullable=False)

    # Relationships
    roles = relationship("Role", secondary="user_roles",
                         back_populates="users")
    address = relationship("Address", uselist=False, back_populates="user")
    invoices = relationship("Invoice", back_populates="user")
    carts = relationship("Cart", back_populates="user")
    wishlist = relationship("WishList", back_populates="user", uselist=False)

    def has_role(self, role_name):

        role_name = role_name.lower()
        return any(role.name == role_name for role in self.roles)


class Role(BaseModel):
    __tablename__ = "roles"

    name = Column(String(255), nullable=False)

    # Relationships
    users = relationship("User", secondary="user_roles",
                         back_populates="roles")


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)


class Address(BaseModel):
    __tablename__ = "addresses"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    address_line = Column(String(255), nullable=False)
    city = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)

    # Relationships
    user = relationship("User", back_populates="address")


class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String(255), nullable=False)
    nutriScore = Column(String(50), nullable=False)
    barCode = Column(String(255), nullable=False)
    picture = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    brand = Column(String(255))
    category_id = Column(Integer, ForeignKey(
        "categories.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(String(255))
    nutrition = Column(JSON)
    ingredients = Column(Text)
    allergens = Column(String(255))
    stock = relationship("Stock", back_populates="product", uselist=False,
                         cascade="all, delete-orphan", passive_deletes=True)
    invoice_items = relationship("InvoiceItem", back_populates="product",
                                 cascade="all, delete-orphan", passive_deletes=True)
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product",
                              cascade="all, delete-orphan", passive_deletes=True)
    wishlist_items = relationship("WishListItem", back_populates="product",
                                  cascade="all, delete-orphan", passive_deletes=True)


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String(255), nullable=False)

    # Relationships
    products = relationship("Product", back_populates="category",)


class Invoice(BaseModel):
    __tablename__ = "invoices"

    total_amount = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    payment_status = Column(String(50), nullable=True)
    paypal_capture_id = Column(String(255), nullable=True)
    paypal_order_id = Column(String(255), nullable=True)
    # Relationships
    user = relationship("User", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice")


class InvoiceItem(BaseModel):
    __tablename__ = "invoice_items"

    product_id = Column(Integer, ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=True)
    quantity = Column(Integer, nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    unit_price = Column(Float, nullable=False)

    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product", back_populates="invoice_items")


class CartStatus(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Cart(BaseModel):
    __tablename__ = "carts"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(
        Enum(CartStatus, name="cartstatus", create_type=True),
        nullable=False,
        default=CartStatus.PENDING,
    )
    # Relationships
    user = relationship("User", back_populates="carts")
    items = relationship("CartItem", back_populates="cart", lazy="joined")


class CartItem(BaseModel):
    __tablename__ = "cart_items"

    product_id = Column(Integer, ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    cart_id = Column(Integer, ForeignKey(
        "carts.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", lazy="joined")

    @property
    def price(self):
        return self.quantity * (self.product.price if self.product else 0)


class Stock(BaseModel):
    __tablename__ = "stocks"
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    quantity = Column(Integer, nullable=False, default=0)
    # Relationships
    product = relationship("Product", back_populates="stock")


class KPI(BaseModel):
    __tablename__ = "kpis"

    name = Column(String(255), nullable=False)
    value = Column(Float, nullable=True)


class BlacklistToken(BaseModel):
    __tablename__ = "blacklist_tokens"

    token = Column(String, unique=True, index=True)


class WishList(BaseModel):
    __tablename__ = "wishlists"

    user_id = Column(Integer, ForeignKey("users.id"),
                     unique=True, nullable=False)

    user = relationship("User", back_populates="wishlist", uselist=False)

    items = relationship(
        "WishListItem", back_populates="wishlist", cascade="all, delete-orphan")


class WishListItem(BaseModel):
    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wishlist_id = Column(Integer, ForeignKey("wishlists.id"), nullable=False)
    product_id = Column(Integer, ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False)

    wishlist = relationship("WishList", back_populates="items")
    product = relationship("Product")
