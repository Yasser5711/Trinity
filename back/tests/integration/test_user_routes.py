def test_get_users(client, admin_auth_header, sample_user):
    response = client.get("/admin/users", headers=admin_auth_header)
    assert response.status_code == 200
    assert any(u["email"] == sample_user.email for u in response.json())


def test_get_user_by_id(client, admin_auth_header, sample_user):
    response = client.get(f"/admin/users/{sample_user.id}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["email"] == sample_user.email


def test_create_user(client, admin_auth_header, sample_role):
    payload = {
        "first_name": "New",
        "last_name": "User",
        "email": "newusertest@example.com",
        "phone": "1234567890",
        "password": "securepass",
        "role_id": sample_role.id,
    }
    response = client.post("/admin/users", json=payload, headers=admin_auth_header)
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"


def test_update_user(client, admin_auth_header, sample_user):
    update_payload = {"first_name": "Updated", "last_name": "User"}
    response = client.put(
        f"/admin/users/{sample_user.id}", json=update_payload, headers=admin_auth_header
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"


def test_delete_user(client, admin_auth_header, sample_user):
    response = client.delete(
        f"/admin/users/{sample_user.id}", headers=admin_auth_header
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
