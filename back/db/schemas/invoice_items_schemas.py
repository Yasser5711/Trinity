from typing import Optional

from .schemas import BaseSchema


class InvoiceItemCreate(BaseSchema):
    invoice_id: int
    product_id: int
    quantity: int
    unit_price: float


class InvoiceItemUpdate(BaseSchema):
    quantity: Optional[int] = None
    unit_price: Optional[float] = None


class InvoiceItemResponse(BaseSchema):
    id: int
    invoice_id: int
    product_id: int
    quantity: int
    unit_price: float
