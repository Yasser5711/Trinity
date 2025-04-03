import services.auth_service as auth_service
from core.helpers.jwt import create_access_token
from db.schemas.auth_schemas import ResetPass, UserCreate, UserLogin, UserUpdateInfo


def test_register_user_success(db_session):
    user_data = UserCreate(
        first_name="Jane",
        last_name="Doe",
        email="janedoe@test.com",
        password="123456",  # noqa: S106
    )
    user = auth_service.register_user(db_session, user_data)
    assert user.email == user_data.email


def test_login_user_success(db_session, sample_user):
    creds = UserLogin(email=sample_user.email, password="password123")  # noqa: S106
    token = auth_service.login_user(db_session, creds)
    assert token


def test_update_current_user(db_session, sample_user):
    updated = auth_service.update_current_user(
        db_session, sample_user.id, UserUpdateInfo(first_name="Neo")
    )
    assert updated.first_name == "Neo"


def test_blacklist_token(db_session):
    token = create_access_token({"sub": "123"})
    auth_service.blacklist_user_token(db_session, token)


def test_reset_password_success(db_session, sample_user):
    token = create_access_token({"sub": str(sample_user.id)})
    reset_data = ResetPass(token=token, password="newpass", confirm_password="newpass")  # noqa: S106
    result = auth_service.reset_password(db_session, reset_data)
    assert result["message"] == "Password reset successfully"
