from datetime import datetime
from typing import Optional

from .schemas import BaseSchema


class StockCreate(BaseSchema):
    product_id: int
    quantity: int


class StockUpdate(BaseSchema):
    quantity: Optional[int] = None


class StockResponse(BaseSchema):
    id: int
    product_id: int
    quantity: int
    updated_at: Optional[datetime] = None
