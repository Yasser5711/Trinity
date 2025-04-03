from db.schemas.cart_schemas import CartStatusEnum


def test_get_cart_statuses(client):
    response = client.get("/carts/status")
    assert response.status_code == 200

    data = response.json()
    assert "statuses" in data
    assert set(data["statuses"]) == {status.value for status in CartStatusEnum}


def test_create_cart_route(client, sample_user, admin_auth_header):
    payload = {"user_id": sample_user.id}
    response = client.post("/carts", json=payload, headers=admin_auth_header)

    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert data["message"] == "Cart created successfully"
    assert "cart_id" in data


def test_create_cart_duplicate_route(client, sample_cart, admin_auth_header):
    payload = {"user_id": sample_cart.user_id}
    response = client.post("/carts", json=payload, headers=admin_auth_header)

    assert response.status_code == 400
    assert response.json()["detail"] == "Cart already exists"


def test_get_cart_by_id_route(client, sample_cart, admin_auth_header):
    response = client.get(f"/carts/{sample_cart.id}", headers=admin_auth_header)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == sample_cart.id
    assert data["user_id"] == sample_cart.user_id
    assert data["status"] == sample_cart.status.value


def test_get_cart_by_id_not_found_route(client, admin_auth_header):
    response = client.get("/carts/9999", headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cart not found"


def test_update_cart_success_route(client, sample_cart, admin_auth_header):
    payload = {"status": "completed"}  # Valid string per CartStatusEnum
    response = client.put(
        f"/carts/{sample_cart.id}", json=payload, headers=admin_auth_header
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Cart updated successfully"


def test_update_cart_invalid_status_route(client, sample_cart, admin_auth_header):
    payload = {"status": "INVALID_STATUS"}  # Not part of CartStatusEnum
    response = client.put(
        f"/carts/{sample_cart.id}", json=payload, headers=admin_auth_header
    )

    assert response.status_code == 422  # Pydantic catches this
    assert response.json()["detail"][0]["msg"].startswith("Input should be")


def test_delete_cart_success_route(client, sample_cart, admin_auth_header):
    response = client.delete(f"/carts/{sample_cart.id}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "Cart deleted successfully"


def test_delete_cart_not_found_route(client, admin_auth_header):
    response = client.delete("/carts/9999", headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cart not found"
