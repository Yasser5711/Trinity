import pytest
import services.user_service as user_service
from db.schemas.users_schemas import UserCreate, UserUpdate


def test_create_user(db_session):
    data = UserCreate(
        first_name="Alice",
        last_name="Doe",
        email="alice@example.com",
        phone="1234567890",
        password="secret",
        role_id=None
    )
    user = user_service.create_user(db_session, data)
    assert user.id
    assert user.email == "alice@example.com"


def test_get_user_by_id(db_session, sample_user):
    user = user_service.get_user_by_id(db_session, sample_user.id)
    assert user.email == sample_user.email


def test_update_user(db_session, sample_user):
    updated = user_service.update_user(
        db_session,
        sample_user.id,
        UserUpdate(first_name="Updated")
    )
    assert updated.first_name == "Updated"


def test_delete_user(db_session, sample_user):
    user_service.delete_user(db_session, sample_user.id)
    with pytest.raises(ValueError):
        user_service.get_user_by_id(db_session, sample_user.id)
