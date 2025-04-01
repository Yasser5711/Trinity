from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.helpers import has_role, get_db
from db.models.models import User
from db.schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse_, CategoryResponse
from services import category_service

router = APIRouter()


@router.get("/categories", response_model=list[CategoryResponse_], tags=["categories"])
def get_categories(
    db: Session = Depends(get_db),
    top: int = Query(None, ge=3, le=10,
                     description="Top N categories by product count")
):
    return category_service.get_categories(db, top)


@router.post("/categories", response_model=CategoryResponse, tags=["categories"], status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin"))
):
    try:
        return category_service.create_category(db, category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/categories/{id}", response_model=CategoryResponse, tags=["categories"])
def update_category(
    id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin"))
):
    try:
        return category_service.update_category(db, id, category)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/categories/{id}", status_code=204, tags=["categories"])
def delete_category(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role("admin"))
):
    try:
        category_service.delete_category(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
