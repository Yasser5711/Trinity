from sqlalchemy.orm import Session

from core.helpers.bcrypt import hash_password, verify_password
from core.helpers.jwt import create_access_token, verify_token
from db.models.models import User
from db.schemas.auth_schemas import ResetPass, UserCreate, UserLogin, UserUpdateInfo
from repositories import auth_repository


def register_user(db: Session, user_data: UserCreate):
    existing = auth_repository.get_user_by_email(db, user_data.email)
    if existing:
        raise ValueError("Email already registered")

    role = auth_repository.get_role_by_name(db, "user")
    if not role:
        from db.models.models import Role

        role = Role(name="user")
        db.add(role)
        db.commit()
        db.refresh(role)

    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=hash_password(user_data.password),
        roles=[role],
    )
    return auth_repository.create_user(db, new_user)


def login_user(db: Session, user_data: UserLogin) -> str:
    user = auth_repository.get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.password):
        raise ValueError("Invalid credentials")

    return create_access_token(data={"sub": str(user.id)})


def blacklist_user_token(db: Session, token: str):
    if auth_repository.token_is_blacklisted(db, token):
        raise ValueError("Token already blacklisted")
    auth_repository.blacklist_token(db, token)


def forgot_password(db: Session, email: str) -> str:
    user = auth_repository.get_user_by_email(db, email)
    if not user:
        raise ValueError("User not found")
    token = create_access_token(data={"sub": str(user.id)}, time=60)
    return token


def reset_password(db: Session, data: ResetPass):
    user_id = verify_token(f"Bearer {data.token}", db)
    user = auth_repository.get_user_by_id(db, user_id)

    if not user:
        raise ValueError("Invalid token")
    if data.password != data.confirm_password:
        raise ValueError("Passwords do not match")

    user.password = hash_password(data.password)
    db.commit()
    return {"message": "Password reset successfully"}


def add_role(db: Session, user_id: int, role_id: int):
    user = auth_repository.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    role = auth_repository.get_role_by_id(db, role_id)
    if not role:
        raise ValueError("Role not found")
    if role in user.roles:
        raise ValueError("User already has this role")
    auth_repository.add_role_to_user(db, user_id, role)
    return {"message": "Role added to user successfully"}


def remove_role(db: Session, user_id: int, role_id: int):
    user = auth_repository.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    role = auth_repository.get_role_by_id(db, role_id)
    if not role:
        raise ValueError("Role not found")
    if role not in user.roles:
        raise ValueError("User does not have this role")
    auth_repository.remove_role_from_user(db, user_id, role)
    return {"message": "Role removed from user successfully"}


def update_current_user(db: Session, user_id: int, update_data: UserUpdateInfo):
    user = auth_repository.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_current_user(db: Session, user_id: int):
    user = auth_repository.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")

    db.delete(user)
    db.commit()
