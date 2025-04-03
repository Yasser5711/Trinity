from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.helpers import get_db, has_role, login_required
from db.models.models import User
from db.schemas.roles_schemas import RoleCreate, RoleResponse, RoleUpdate
from services import role_service

router = APIRouter()


@router.get("/roles", response_model=list[RoleResponse], tags=["roles"])
def get_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(login_required),
):
    return role_service.list_roles(db)


@router.post("/roles", tags=["roles"])
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        created = role_service.create_role(db, role.name)
        return {"message": "Role created successfully", "role": created}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.put("/roles", tags=["roles"])
def update_role(
    role: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        updated = role_service.update_role(db, role.id, role.name)
        return {"message": "Role updated successfully", "role": updated}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/roles/{role_id}", tags=["roles"])
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        role_service.delete_role(db, role_id)
        return {"message": "Role deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
