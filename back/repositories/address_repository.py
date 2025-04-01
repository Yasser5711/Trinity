from sqlalchemy.orm import Session
from db.models.models import Address
from db.schemas.address_schemas import AddressCreate, AddressUpdate


def get_user_addresses(db: Session, user_id: int):
    return db.query(Address).filter(Address.user_id == user_id).all()


def get_by_id(db: Session, address_id: int, user_id: int):
    return db.query(Address).filter(Address.id == address_id, Address.user_id == user_id).first()


def create(db: Session, user_id: int, address_data: AddressCreate):
    new_address = Address(user_id=user_id, **address_data.model_dump())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


def update(db: Session, address, update_data: AddressUpdate):
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(address, key, value)
    db.commit()
    db.refresh(address)
    return address


def delete(db: Session, address):
    db.delete(address)
    db.commit()
