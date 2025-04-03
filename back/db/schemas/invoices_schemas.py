from datetime import datetime
from typing import List, Optional  # noqa: UP035

from pydantic import BaseModel

from .schemas import Product as ProductResponse
from .schemas import UserBase as UserResponse


class InvoiceItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float


class InvoiceCreate(BaseModel):
    user_id: int
    items: List[InvoiceItemCreate]  # noqa: UP006


class InvoiceUpdate(BaseModel):
    items: List[InvoiceItemCreate]  # noqa: UP006


class InvoiceItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        orm_mode = True


class InvoiceItemResponse_2(BaseModel):  # noqa: N801
    product: ProductResponse
    quantity: int
    unit_price: float

    class Config:
        orm_mode = True


class InvoiceResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    created_at: Optional[datetime]
    items: List[InvoiceItemResponse]  # noqa: UP006
    user: Optional[UserResponse]
    payment_status: Optional[str]

    class Config:
        orm_mode = True


class InvoiceResponse_2(BaseModel):  # noqa: N801
    id: int
    user_id: int
    total_amount: float
    created_at: Optional[datetime]
    items: List[InvoiceItemResponse_2]  # noqa: UP006
    user: Optional[UserResponse]
    payment_status: Optional[str]

    class Config:
        orm_mode = True
