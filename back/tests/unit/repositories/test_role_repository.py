from db.models.models import Role
import repositories.role_repository as role_repository


def test_get_all_roles(db_session, sample_role):
    roles = role_repository.get_all_roles(db_session)
    assert isinstance(roles, list)
    assert sample_role in roles


def test_get_role_by_id(db_session, sample_role):
    role = role_repository.get_role_by_id(db_session, sample_role.id)
    assert role.id == sample_role.id


def test_get_role_by_name(db_session, sample_role):
    role = role_repository.get_role_by_name(db_session, sample_role.name)
    assert role.name == sample_role.name


def test_create_role(db_session):
    new_role = Role(name="developer")
    created = role_repository.create_role(db_session, new_role)
    assert created.id
    assert created.name == "developer"


def test_update_role(db_session, sample_role):
    role_repository.update_role(db_session, sample_role, "lead")
    assert sample_role.name == "lead"


def test_delete_role(db_session, sample_role):
    role_repository.delete_role(db_session, sample_role)
    assert role_repository.get_role_by_id(db_session, sample_role.id) is None
