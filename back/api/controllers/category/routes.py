from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.helpers import get_db, has_role
from db.models.models import User
from db.schemas.category_schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryResponse_,
    CategoryUpdate,
)
from services import category_service

router = APIRouter()


@router.get("/categories", response_model=list[CategoryResponse_], tags=["categories"])
def get_categories(
    db: Session = Depends(get_db),
    top: int = Query(
        None, ge=3, le=10, description="Top N categories by product count"
    ),
):
    return category_service.get_categories(db, top)


@router.post(
    "/categories",
    response_model=CategoryResponse,
    tags=["categories"],
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        return category_service.create_category(db, category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.put(
    "/categories/{category_id}", response_model=CategoryResponse, tags=["categories"]
)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        return category_service.update_category(db, category_id, category)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/categories/{category_id}", status_code=204, tags=["categories"])
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin")),
):
    try:
        category_service.delete_category(db, category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
