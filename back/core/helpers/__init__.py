from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

import db.schemas.auth_schemas as auth_schemas
import db.schemas.roles_schemas as roles_schemas
from db.models import models
from db.session import SessionLocal, get_db

from .bcrypt import hash_password, verify_password
from .jwt import create_access_token, verify_token

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
# def get_api_key(api_key_header: str = Depends(api_key_header)):
#     if api_key_header:
#         return api_key_header
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Unauthorized",
#     )


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


def login_required(token: str = Depends(api_key_header), db: Session = Depends(get_db)):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is missing",
        )

    id = verify_token(token, db)

    if id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    # if not isinstance(id, UUID):
    #     id = UUID(id)
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


def has_role(role: str):
    def role_checker(user: models.User = Depends(login_required)):
        if not user.has_role(role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have the required role",
            )
        return user

    return role_checker
