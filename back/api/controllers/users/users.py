from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.schemas import schemas, users_schemas
from db.models.models import User
from core.helpers import has_role, get_db
from services import user_service

router = APIRouter()


@router.get("/users", response_model=list[schemas.UserBase], tags=["users"])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(has_role("admin"))):
    users = user_service.list_users(db)
    response = []
    for user in users:
        roles = [schemas.RoleBase.from_orm(
            role).model_dump() for role in user.roles]
        base = schemas.UserBase.from_orm(user).model_dump()
        response.append({**base, "roles": roles})
    return response


@router.post("/users", status_code=201, tags=["users"])
def create_user(user: users_schemas.UserCreate, db: Session = Depends(get_db), current_user: User = Depends(has_role("admin"))):
    try:
        user_service.create_user(db, user)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/users/{id}", tags=["users"])
def update_user(id: int, user_update: users_schemas.UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(has_role("admin"))):
    try:
        user_service.update_user(db, id, user_update)
        return {"message": "User updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/users/{id}", tags=["users"])
def delete_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(has_role("admin"))):
    try:
        user_service.delete_user(db, id)
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/users/{id}", tags=["users"])
def get_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(has_role("admin"))):
    try:
        user = user_service.get_user_by_id(db, id)
        base = schemas.UserBase.from_orm(user).model_dump()
        roles = [schemas.RoleBase.from_orm(
            role).model_dump() for role in user.roles]
        return {**base, "roles": roles}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
