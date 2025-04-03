def test_get_cart(client, auth_header):
    response = client.get("/client/cart", headers=auth_header)
    assert response.status_code == 200
    assert "id" in response.json()


def test_add_cart_item(client, auth_header, sample_product):
    payload = {"cart_id": 1, "product_id": sample_product.id, "quantity": 2}
    response = client.post("/client/cart/items", json=payload, headers=auth_header)
    assert response.status_code == 201
    assert response.json()["product_id"] == sample_product.id


def test_update_cart_item(client, auth_header, sample_cart_item):
    payload = {"quantity": 5}
    response = client.put(
        f"/client/cart/items/{sample_cart_item.id}", json=payload, headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 5


def test_remove_cart_item(client, auth_header, sample_cart_item):
    response = client.delete(
        f"/client/cart/items/{sample_cart_item.id}", headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Item removed from cart"


def test_checkout(client, auth_header, sample_cart_item):
    response = client.post("/client/checkout", headers=auth_header)
    assert response.status_code == 201
    assert "total_amount" in response.json()


def test_get_invoices(client, auth_header):
    response = client.get("/client/invoices", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_invoice(client, auth_header, sample_cart_item):
    invoice_response = client.post("/client/checkout", headers=auth_header)
    invoice_id = invoice_response.json()["id"]

    response = client.get(f"/client/invoices/{invoice_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == invoice_id
