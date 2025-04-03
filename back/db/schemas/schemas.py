from datetime import datetime
from typing import List, Optional  # noqa: UP035

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseSchema):
    id: Optional[int] = None
    name: Optional[str] = None


class UserBase(BaseSchema):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    roles: List[RoleBase] = []  # noqa: UP006


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"  # noqa: S105


class Users(BaseModel):
    users: List[UserBase]  # noqa: UP006


class Product(BaseSchema):
    id: Optional[int] = None
    nutriScore: Optional[str] = Field(None, max_length=50)  # noqa: N815
    barCode: Optional[str] = Field(None, max_length=255)  # noqa: N815
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    picture: Optional[str] = None
    price: Optional[float] = None
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    brand: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = None
    quantity: Optional[str] = None
    nutrition: Optional[dict] = None
    ingredients: Optional[str] = None
    allergens: Optional[str] = Field(None, max_length=255)


class KPI(BaseSchema):
    id: Optional[int] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    value: Optional[float] = None
