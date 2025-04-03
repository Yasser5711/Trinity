from decimal import Decimal
from typing import List, Optional  # noqa: UP035

from .category_schemas import CategoryResponse
from .schemas import BaseSchema
from .schemas import Product as ProductBase
from .stock_schemas import StockResponse as StockBase


class ProductCreate(ProductBase):
    name: str
    price: Decimal
    description: str
    category_id: int
    brand: str
    barCode: str  # noqa: N815


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    stock: Optional[StockBase] = None
    category: Optional[CategoryResponse] = None
    pass


class ProductPaginated(BaseSchema):
    products: List[ProductResponse]  # noqa: UP006
    total: int
    total_pages: int
    page: int
    limit: int
    next_page: Optional[int] = None
    prev_page: Optional[int] = None
    message: Optional[str] = None
