import repositories.auth_repository as auth_repository
from db.models.models import BlacklistToken


def test_get_user_by_email(db_session, sample_user):
    found = auth_repository.get_user_by_email(db_session, sample_user.email)
    assert found.id == sample_user.id


def test_blacklist_token_and_check(db_session):
    token = "blacklisted.token"
    auth_repository.blacklist_token(db_session, token)
    assert auth_repository.token_is_blacklisted(db_session, token)


def test_add_remove_role(db_session, sample_user, sample_role):
    auth_repository.add_role_to_user(db_session, sample_user.id, sample_role)
    assert sample_role in sample_user.roles

    auth_repository.remove_role_from_user(
        db_session, sample_user.id, sample_role)
    assert sample_role not in sample_user.roles
