from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.helpers import get_db, has_role
from db.models.models import User
from db.schemas import schemas, users_schemas
from services import user_service

router = APIRouter()


@router.get("/users", response_model=list[schemas.UserBase], tags=["users"])
def get_users(
    db: Session = Depends(get_db), current_user: User = Depends(has_role("admin"))
):
    users = user_service.list_users(db)
    response = []
    for user in users:
        roles = [schemas.RoleBase.from_orm(role).model_dump() for role in user.roles]
        base = schemas.UserBase.from_orm(user).model_dump()
        response.append({**base, "roles": roles})
    return response


@router.post("/users", status_code=201, tags=["users"])
def create_user(
    user: users_schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        user_service.create_user(db, user)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.put("/users/{user_id}", tags=["users"])
def update_user(
    user_id: int,
    user_update: users_schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        user_service.update_user(db, user_id, user_update)
        return {"message": "User updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/users/{user_id}", tags=["users"])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        user_service.delete_user(db, user_id)
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/users/{user_id}", tags=["users"])
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        user = user_service.get_user_by_id(db, user_id)
        base = schemas.UserBase.from_orm(user).model_dump()
        roles = [schemas.RoleBase.from_orm(role).model_dump() for role in user.roles]
        return {**base, "roles": roles}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
