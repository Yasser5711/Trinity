from sqlalchemy.orm import Session
from db.models.models import Role
from repositories import role_repository


def list_roles(db: Session):
    return role_repository.get_all_roles(db)


def create_role(db: Session, name: str):
    name = name.lower()
    if role_repository.get_role_by_name(db, name):
        raise ValueError("Role already exists")
    return role_repository.create_role(db, Role(name=name))


def update_role(db: Session, role_id: int, name: str):
    role = role_repository.get_role_by_id(db, role_id)
    if not role:
        raise ValueError("Role not found")
    return role_repository.update_role(db, role, name.lower())


def delete_role(db: Session, role_id: int):
    role = role_repository.get_role_by_id(db, role_id)
    if not role:
        raise ValueError("Role not found")
    role_repository.delete_role(db, role)
