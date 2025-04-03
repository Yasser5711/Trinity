def test_get_cart_items(client, admin_auth_header, sample_cart_item):
    response = client.get("/cart-items", headers=admin_auth_header)
    assert response.status_code == 200
    assert any(item["id"] == sample_cart_item.id for item in response.json())


def test_get_cart_item_by_id(client, admin_auth_header, sample_cart_item):
    response = client.get(
        f"/cart-items/{sample_cart_item.id}", headers=admin_auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_cart_item.id


def test_get_cart_item_by_invalid_id(client, admin_auth_header):
    response = client.get("/cart-items/9999", headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cart item not found"


def test_create_cart_item(client, admin_auth_header, sample_cart, sample_product):
    payload = {
        "cart_id": sample_cart.id,
        "product_id": sample_product.id,
        "quantity": 3,
    }
    response = client.post("/cart-items", json=payload, headers=admin_auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Cart item added successfully"
    assert data["price"] == 30.0


def test_create_cart_item_invalid_product(client, admin_auth_header, sample_cart):
    payload = {"cart_id": sample_cart.id, "product_id": 9999, "quantity": 1}
    response = client.post("/cart-items", json=payload, headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_update_cart_item(client, admin_auth_header, sample_cart_item):
    payload = {"quantity": 5}
    response = client.put(
        f"/cart-items/{sample_cart_item.id}", json=payload, headers=admin_auth_header
    )
    assert response.status_code == 200
    assert response.json()["price"] == 50.0


def test_update_cart_item_not_found(client, admin_auth_header):
    payload = {"quantity": 5}
    response = client.put("/cart-items/9999", json=payload, headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cart item not found"


def test_delete_cart_item(client, admin_auth_header, sample_cart_item):
    response = client.delete(
        f"/cart-items/{sample_cart_item.id}", headers=admin_auth_header
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Cart item deleted successfully"


def test_delete_cart_item_not_found(client, admin_auth_header):
    response = client.delete("/cart-items/9999", headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cart item not found"
