import repositories.user_repository as user_repository
from db.models.models import User


def test_get_all_users(db_session, sample_user):
    users = user_repository.get_all_users(db_session)
    assert sample_user in users


def test_get_user_by_email(db_session, sample_user):
    user = user_repository.get_user_by_email(db_session, sample_user.email)
    assert user.id == sample_user.id


def test_get_user_by_id(db_session, sample_user):
    user = user_repository.get_user_by_id(db_session, sample_user.id)
    assert user.email == sample_user.email


def test_create_and_delete_user(db_session):
    user = User(
        first_name="Delete",
        last_name="Me",
        email="deleteme@example.com",
        phone="0000000000",
        password="hashed",  # noqa: S106
    )
    created = user_repository.create_user(db_session, user)
    assert created.id

    user_repository.delete_user(db_session, created)
    assert user_repository.get_user_by_id(db_session, created.id) is None
