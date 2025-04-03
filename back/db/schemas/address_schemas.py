from typing import Optional

from pydantic import BaseModel


class AddressBase(BaseModel):
    address_line: str
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None


class AddressCreate(AddressBase):
    address_line: str


class AddressUpdate(AddressBase):
    address_line: Optional[str] = None


class AddressResponse(AddressBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
