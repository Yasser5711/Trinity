def test_get_wishlist(client, auth_header):
    response = client.get("/client/wishlist", headers=auth_header)
    assert response.status_code == 200
    assert "items" in response.json()


def test_add_to_wishlist(client, auth_header, sample_product):
    payload = {"product_id": sample_product.id}
    response = client.post("/client/wishlist/items", json=payload, headers=auth_header)
    assert response.status_code == 201
    assert any(
        item["product"]["id"] == sample_product.id for item in response.json()["items"]
    )


def test_add_existing_product_to_wishlist_fails(client, auth_header, sample_product):
    payload = {"product_id": sample_product.id}
    client.post(
        "/client/wishlist/items", json=payload, headers=auth_header
    )  # First add
    response = client.post(
        "/client/wishlist/items", json=payload, headers=auth_header
    )  # Second add
    assert response.status_code == 400
    assert response.json()["detail"] == "Product already in wishlist"


def test_remove_from_wishlist(client, auth_header, sample_product):
    payload = {"product_id": sample_product.id}
    client.post("/client/wishlist/items", json=payload, headers=auth_header)
    response = client.delete(
        f"/client/wishlist/items/{sample_product.id}", headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Product removed from wishlist"


def test_delete_wishlist(client, auth_header, sample_product):
    client.post(
        "/client/wishlist/items",
        json={"product_id": sample_product.id},
        headers=auth_header,
    )
    response = client.delete("/client/wishlist", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "Wishlist deleted successfully"
