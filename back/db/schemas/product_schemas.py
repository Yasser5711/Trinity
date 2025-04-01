from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel

from .schemas import Product as ProductBase, BaseSchema
from .stock_schemas import StockResponse as StockBase
from .category_schemas import CategoryResponse


class ProductCreate(ProductBase):
    name: str
    price: Decimal
    description: str
    category_id: int
    brand: str
    barCode: str


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    stock: Optional[StockBase] = None
    category: Optional[CategoryResponse] = None
    pass


class ProductPaginated(BaseSchema):
    products: List[ProductResponse]
    total: int
    total_pages: int
    page: int
    limit: int
    next_page: Optional[int] = None
    prev_page: Optional[int] = None
    message: Optional[str] = None
