from typing import List, Optional  # noqa: UP035

from pydantic import BaseModel, EmailStr

from .schemas import RoleBase as Role
from .schemas import UserBase as UserSchema


class Roles(Role):
    id: int
    name: str


class User(UserSchema):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    roles: List[Roles]  # noqa: UP006


class UserCreate(UserSchema):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserUpdateInfo(UserSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    class Config:
        extra = "forbid"
        orm_mode = True


class UserUpdate(UserSchema):
    id: int
    pass


class UserPasswordUpdate(UserSchema):
    email: EmailStr
    password: str


class UserLogin(UserSchema):
    email: EmailStr
    password: str


class UserRoleRequest(BaseModel):
    user_id: int
    role_id: int


class ForgotPass(BaseModel):
    email: EmailStr


class ForgotPassResponse(BaseModel):
    message: str
    token: str


class ResetPass(BaseModel):
    token: str
    password: str
    confirm_password: str
