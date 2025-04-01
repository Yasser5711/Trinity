import pytest


def test_get_roles(client, auth_header):
    response = client.get("/admin/roles", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_role(client, admin_auth_header):
    payload = {"name": "moderator"}
    response = client.post("/admin/roles", json=payload,
                           headers=admin_auth_header)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["role"]["name"] == "moderator"
    assert "Role created successfully" in json_data["message"]


def test_create_duplicate_role_fails(client, admin_auth_header):
    payload = {"name": "admin"}  # assuming this already exists
    response = client.post("/admin/roles", json=payload,
                           headers=admin_auth_header)
    assert response.status_code == 400
    assert response.json()["detail"] == "Role already exists"


def test_update_role(client, admin_auth_header, sample_role):
    payload = {
        "id": sample_role.id,
        "name": "superadmin"
    }
    response = client.put("/admin/roles", json=payload,
                          headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["role"]["name"] == "superadmin"


def test_update_nonexistent_role(client, admin_auth_header):
    payload = {
        "id": 9999,
        "name": "ghost"
    }
    response = client.put("/admin/roles", json=payload,
                          headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Role not found"


def test_delete_role(client, admin_auth_header, sample_role):
    response = client.delete(
        f"/admin/roles/{sample_role.id}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "Role deleted successfully"


def test_delete_nonexistent_role(client, admin_auth_header):
    response = client.delete("/admin/roles/9999", headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Role not found"
