from typing import Optional

from .auth_schemas import UserCreate as UserCreatee
from .auth_schemas import UserUpdate


class UserCreate(UserCreatee):
    password: Optional[str] = None
    role_id: Optional[int] = None


class UserUpdate(UserUpdate):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
