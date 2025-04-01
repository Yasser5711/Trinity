from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.helpers import login_required
from db.models.models import User
from db.schemas.address_schemas import AddressResponse, AddressCreate, AddressUpdate
from db.session import get_db
from services import address_service

router = APIRouter()


@router.get("/addresses", response_model=list[AddressResponse], tags=["addresses"])
def get_addresses(
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db),
):
    return address_service.list_user_addresses(db, current_user.id)


@router.post("/addresses", response_model=AddressResponse, status_code=status.HTTP_201_CREATED, tags=["addresses"])
def create_address(
    address: AddressCreate,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db),
):
    return address_service.create_address(db, current_user.id, address)


@router.get("/addresses/{address_id}", response_model=AddressResponse, tags=["addresses"])
def get_address_by_id(
    address_id: int,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db),
):
    address = address_service.get_address_by_id(
        db, address_id, current_user.id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.put("/addresses/{address_id}", response_model=AddressResponse, tags=["addresses"])
def update_address(
    address_id: int,
    address_update: AddressUpdate,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db),
):
    address = address_service.get_address_by_id(
        db, address_id, current_user.id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return address_service.update_address(db, address, address_update)


@router.delete("/addresses/{address_id}", status_code=status.HTTP_200_OK, tags=["addresses"])
def delete_address(
    address_id: int,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db),
):
    address = address_service.get_address_by_id(
        db, address_id, current_user.id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    address_service.delete_address(db, address)
    return {"message": "Address deleted successfully"}
