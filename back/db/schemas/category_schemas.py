
from .schemas import BaseSchema


class CategoryCreate(BaseSchema):
    name: str


class CategoryUpdate(BaseSchema):
    name: str


class CategoryResponse_(BaseSchema):
    id: int
    name: str
    product_count: int


class CategoryResponse(BaseSchema):
    id: int
    name: str
