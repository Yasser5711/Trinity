import pytest

import services.role_service as role_service
from db.models.models import Role


def test_list_roles(db_session, sample_role):
    roles = role_service.list_roles(db_session)
    assert any(role.id == sample_role.id for role in roles)


def test_create_role(db_session):
    role = role_service.create_role(db_session, "tester")
    assert role.id
    assert role.name == "tester"


def test_create_duplicate_role_raises(db_session, sample_role):
    with pytest.raises(ValueError, match="Role already exists"):
        role_service.create_role(db_session, sample_role.name)


def test_update_role(db_session, sample_role):
    updated = role_service.update_role(db_session, sample_role.id, "updated-role")
    assert updated.name == "updated-role"


def test_update_nonexistent_role_raises(db_session):
    with pytest.raises(ValueError, match="Role not found"):
        role_service.update_role(db_session, 9999, "ghost")


def test_delete_role(db_session, sample_role):
    role_service.delete_role(db_session, sample_role.id)
    assert db_session.query(Role).filter(Role.id == sample_role.id).first() is None


def test_delete_nonexistent_role_raises(db_session):
    with pytest.raises(ValueError, match="Role not found"):
        role_service.delete_role(db_session, 9999)
