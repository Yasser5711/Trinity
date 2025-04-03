from datetime import datetime
from enum import Enum
from typing import List, Optional  # noqa: UP035

from .schemas import BaseSchema


class CartStatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CartItemResponse(BaseSchema):
    id: int
    product_id: int
    quantity: int
    price: float


class CartCreate(BaseSchema):
    user_id: int


class CartUpdate(BaseSchema):
    status: Optional[CartStatusEnum]


class CartResponse(BaseSchema):
    id: int
    user_id: int
    created_at: datetime
    status: CartStatusEnum


class CartDetailResponse(CartResponse):
    items: List[CartItemResponse]  # noqa: UP006


class CartStatusResponse(BaseSchema):
    statuses: List[str]  # noqa: UP006
