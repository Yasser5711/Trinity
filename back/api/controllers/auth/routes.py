from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.helpers import api_key_header, get_db, has_role, login_required
from db.models.models import User as UserModel
from db.schemas.auth_schemas import (
    ForgotPass,
    ForgotPassResponse,
    ResetPass,
    User,
    UserCreate,
    UserLogin,
    UserRoleRequest,
    UserUpdateInfo,
)
from db.schemas.schemas import Token
from services import auth_service

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED, tags=["auth"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        auth_service.register_user(db, user)
        return {"detail": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post(
    "/login", response_model=Token, status_code=status.HTTP_200_OK, tags=["auth"]
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        token = auth_service.login_user(db, user)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/me", response_model=User, status_code=status.HTTP_200_OK, tags=["auth"])
def me(current_user: UserModel = Depends(login_required)):
    return current_user


@router.put("/me", response_model=User, tags=["auth"])
def update_user(
    user: UserUpdateInfo,
    db: Session = Depends(get_db),
    current_user: User = Depends(login_required),
):
    try:
        return auth_service.update_current_user(db, current_user.id, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/me", tags=["auth"])
def delete_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(login_required),
):
    try:
        auth_service.delete_current_user(db, current_user.id)
        return {"message": "Account deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/logout", status_code=status.HTTP_200_OK, tags=["auth"])
def logout(token: str = Depends(api_key_header), db: Session = Depends(get_db)):
    token = token.replace("Bearer ", "")
    try:
        auth_service.blacklist_user_token(db, token)
        return {"message": "Logged out successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid token") from None


@router.post("/forgot-password", response_model=ForgotPassResponse, tags=["auth"])
def forgot_password(data: ForgotPass, db: Session = Depends(get_db)):
    try:
        token = auth_service.forgot_password(db, data.email)
        return {"message": "Token has 1hour", "token": token}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/reset-password", tags=["auth"])
def reset_password(data: ResetPass, db: Session = Depends(get_db)):
    try:
        return auth_service.reset_password(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/roles", tags=["auth"])
def add_role_to_user(
    request: UserRoleRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(has_role("admin")),
):
    try:
        return auth_service.add_role(db, request.user_id, request.role_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/roles", tags=["auth"])
def remove_role_from_user(
    request: UserRoleRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(has_role("admin")),
):
    try:
        return auth_service.remove_role(db, request.user_id, request.role_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
