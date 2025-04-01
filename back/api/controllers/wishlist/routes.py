from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.helpers import login_required, get_db
from db.models.models import User
from db.schemas.wishlist_schemas import WishlistResponse, WishlistAddItem
from services import wishlist_service

router = APIRouter()


@router.get("/wishlist", response_model=WishlistResponse, tags=["wishlist"])
def get_wishlist(
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    return wishlist_service.get_or_create_wishlist(db, current_user.id)


@router.post("/wishlist/items", response_model=WishlistResponse, status_code=status.HTTP_201_CREATED, tags=["wishlist"])
def add_to_wishlist(
    item: WishlistAddItem,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    try:
        return wishlist_service.add_to_wishlist(db, current_user.id, item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/wishlist/items/{product_id}", tags=["wishlist"])
def remove_from_wishlist(
    product_id: int,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    try:
        wishlist_service.remove_from_wishlist(db, current_user.id, product_id)
        return {"message": "Product removed from wishlist"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/wishlist", tags=["wishlist"])
def delete_wishlist(
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    try:
        wishlist_service.delete_wishlist(db, current_user.id)
        return {"message": "Wishlist deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
