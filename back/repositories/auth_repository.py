from sqlalchemy.orm import Session
from db.models.models import User, Role, BlacklistToken


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_role_by_name(db: Session, name: str) -> Role | None:
    return db.query(Role).filter(Role.name == name).first()


def get_role_by_id(db: Session, role_id: int) -> Role | None:
    return db.query(Role).filter(Role.id == role_id).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def token_is_blacklisted(db: Session, token: str) -> bool:
    return db.query(BlacklistToken).filter(BlacklistToken.token == token).first() is not None


def blacklist_token(db: Session, token: str):
    blacklisted = BlacklistToken(token=token)
    db.add(blacklisted)
    db.commit()


def add_role_to_user(db: Session, user_id: int, role):
    user = get_user_by_id(db, user_id)
    if role not in user.roles:
        user.roles.append(role)
        db.commit()


def remove_role_from_user(db: Session, user_id: int, role):
    user = get_user_by_id(db, user_id)
    if role in user.roles:
        user.roles.remove(role)
        db.commit()
