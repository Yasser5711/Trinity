from datetime import datetime
from typing import List, Optional
from .schemas import UserBase as UserResponse, Product as ProductResponse
from pydantic import BaseModel


class InvoiceItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float


class InvoiceCreate(BaseModel):
    user_id: int
    items: List[InvoiceItemCreate]


class InvoiceUpdate(BaseModel):
    items: List[InvoiceItemCreate]


class InvoiceItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        orm_mode = True


class InvoiceItemResponse_2(BaseModel):
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
    items: List[InvoiceItemResponse]
    user: Optional[UserResponse]
    payment_status: Optional[str]

    class Config:
        orm_mode = True


class InvoiceResponse_2(BaseModel):
    id: int
    user_id: int
    total_amount: float
    created_at: Optional[datetime]
    items: List[InvoiceItemResponse_2]
    user: Optional[UserResponse]
    payment_status: Optional[str]

    class Config:
        orm_mode = True
