from sqlalchemy.orm import Session
from db.models.models import User
from db.schemas.users_schemas import UserCreate, UserUpdate
from core.helpers.bcrypt import hash_password
from repositories import user_repository


def list_users(db: Session):
    return user_repository.get_all_users(db)


def create_user(db: Session, data: UserCreate):
    if user_repository.get_user_by_email(db, data.email):
        raise ValueError("Email already registered")

    password = hash_password(data.password or "000000")
    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone=data.phone,
        password=password
    )

    user = user_repository.create_user(db, user)

    if data.role_id:
        role = user_repository.get_role_by_id(db, data.role_id)
        if not role:
            raise ValueError("Role not found")
        user.roles.append(role)
        db.commit()

    return user


def update_user(db: Session, user_id: int, data: UserUpdate):
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")

    if data.email and data.email != user.email:
        if user_repository.get_user_by_email(db, data.email):
            raise ValueError("Email already in use")
        user.email = data.email

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")

    cart = user_repository.get_cart_by_user_id(db, user_id)
    if cart:
        user_repository.delete_cart_and_items(db, cart)

    user_repository.delete_user(db, user)


def get_user_by_id(db: Session, user_id: int):
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    return user
