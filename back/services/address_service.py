from sqlalchemy.orm import Session
from db.schemas.address_schemas import AddressCreate, AddressUpdate
from db.models.models import Address
from repositories import address_repository


def list_user_addresses(db: Session, user_id: int) -> list[Address]:
    return address_repository.get_user_addresses(db, user_id)


def get_address_by_id(db: Session, address_id: int, user_id: int) -> Address | None:
    return address_repository.get_by_id(db, address_id, user_id)


def create_address(db: Session, user_id: int, address_data: AddressCreate) -> Address:
    return address_repository.create(db, user_id, address_data)


def update_address(db: Session, address: Address, address_data: AddressUpdate) -> Address:
    return address_repository.update(db, address, address_data)


def delete_address(db: Session, address: Address) -> None:
    address_repository.delete(db, address)
