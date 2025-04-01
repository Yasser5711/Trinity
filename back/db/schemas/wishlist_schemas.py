from pydantic import BaseModel
from typing import List
from .product_schemas import ProductResponse


class WishlistItemBase(BaseModel):
    product_id: int


class WishlistItemResponse(WishlistItemBase):
    id: int
    product: ProductResponse

    class Config:
        orm_mode = True


class WishlistCreate(BaseModel):
    pass


class WishlistResponse(BaseModel):
    id: int
    # user_id: int
    items: List[WishlistItemResponse]

    class Config:
        orm_mode = True


class WishlistAddItem(BaseModel):
    product_id: int
