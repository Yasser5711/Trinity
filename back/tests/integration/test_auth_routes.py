from core.helpers.jwt import create_access_token


def test_register_user(client, db_session):
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "newuser@example.com",
        "password": "securepass123",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    assert response.json()["detail"] == "User created successfully"


def test_login_user(client, sample_user):
    response = client.post(
        "/auth/login", json={"email": sample_user.email, "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_me(client, auth_header):
    response = client.get("/auth/me", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["email"]


def test_update_me(client, auth_header):
    response = client.put(
        "/auth/me", headers=auth_header, json={"first_name": "Changed"}
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Changed"


def test_delete_me(client, auth_header):
    response = client.delete("/auth/me", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "Account deleted successfully"


def test_logout(client, auth_header):
    response = client.post("/auth/logout", headers=auth_header)
    assert response.status_code == 200


def test_forgot_password(client, sample_user):
    response = client.post("/auth/forgot-password", json={"email": sample_user.email})
    assert response.status_code == 200
    assert "token" in response.json()


def test_reset_password(client, db_session, sample_user):
    token = create_access_token({"sub": str(sample_user.id)})
    response = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "password": "newpass123",
            "confirm_password": "newpass123",
        },
    )
    assert response.status_code == 200


def test_add_remove_role(client, admin_auth_header, sample_user, sample_role):
    data = {"user_id": sample_user.id, "role_id": sample_role.id}
    r_add = client.post("/auth/roles", json=data, headers=admin_auth_header)
    assert r_add.status_code == 200

    r_remove = client.request(
        method="DELETE", url="/auth/roles", headers=admin_auth_header, json=data
    )
    assert r_remove.status_code == 200
