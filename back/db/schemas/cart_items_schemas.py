from typing import Optional

from .schemas import BaseSchema


class CartItemCreate(BaseSchema):
    cart_id: int
    product_id: int
    quantity: int


class CartItemUpdate(BaseSchema):
    quantity: Optional[int] = None
    price: Optional[float] = None


class CartItemResponse(BaseSchema):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    price: float
