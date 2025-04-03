from sqlalchemy.orm import Session

from db.models.models import Role


def get_all_roles(db: Session):
    return db.query(Role).all()


def get_role_by_id(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()


def create_role(db: Session, role: Role):
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: Session, role: Role, name: str):
    role.name = name
    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role: Role):
    db.delete(role)
    db.commit()
