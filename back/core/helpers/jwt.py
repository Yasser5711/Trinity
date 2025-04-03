from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.config import settings
from db.models import models

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, time=ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=time)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, db: Session):
    try:
        token = token.split("Bearer ")[1]
        db_token = (
            db.query(models.BlacklistToken)
            .filter(models.BlacklistToken.token == token)
            .first()
        )
        if db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token blacklisted",
            )
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")  # noqa: A001
        if id is None:
            return None
        return id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
        ) from JWTError
