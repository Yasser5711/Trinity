def test_create_invoice_item(client, admin_auth_header, sample_product, sample_user):
    invoice_payload = {
        "user_id": sample_user.id,
        "items": [{"product_id": sample_product.id, "quantity": 1, "price": 10.0}],
    }
    invoice = client.post(
        "/invoices", json=invoice_payload, headers=admin_auth_header
    ).json()

    payload = {
        "invoice_id": invoice["id"],
        "product_id": sample_product.id,
        "quantity": 2,
        "unit_price": 20.0,
    }

    response = client.post("/invoice-items", json=payload, headers=admin_auth_header)
    assert response.status_code == 201
    assert response.json()["quantity"] == 2
    assert response.json()["invoice_id"] == invoice["id"]


def test_get_invoice_items(client, admin_auth_header):
    response = client.get("/invoice-items", headers=admin_auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_invoice_item_by_id(client, admin_auth_header, sample_product, sample_user):
    invoice = client.post(
        "/invoices",
        json={
            "user_id": sample_user.id,
            "items": [{"product_id": sample_product.id, "quantity": 1, "price": 15.0}],
        },
        headers=admin_auth_header,
    ).json()

    # invoice_item_id = invoice["items"][0]["product_id"]
    all_items = client.get("/invoice-items", headers=admin_auth_header).json()
    matching = next((i for i in all_items if i["invoice_id"] == invoice["id"]), None)

    assert matching
    response = client.get(f"/invoice-items/{matching['id']}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == matching["id"]


def test_update_invoice_item(client, admin_auth_header, sample_product, sample_user):
    invoice = client.post(
        "/invoices",
        json={
            "user_id": sample_user.id,
            "items": [{"product_id": sample_product.id, "quantity": 1, "price": 10.0}],
        },
        headers=admin_auth_header,
    ).json()

    # item_id = invoice["items"][0]["product_id"]
    all_items = client.get("/invoice-items", headers=admin_auth_header).json()
    item = next((i for i in all_items if i["invoice_id"] == invoice["id"]), None)

    response = client.put(
        f"/invoice-items/{item['id']}",
        json={"quantity": 5, "unit_price": 12.5},
        headers=admin_auth_header,
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Invoice item updated successfully"


def test_delete_invoice_item(client, admin_auth_header, sample_product, sample_user):
    invoice = client.post(
        "/invoices",
        json={
            "user_id": sample_user.id,
            "items": [{"product_id": sample_product.id, "quantity": 1, "price": 8.0}],
        },
        headers=admin_auth_header,
    ).json()

    all_items = client.get("/invoice-items", headers=admin_auth_header).json()
    item = next((i for i in all_items if i["invoice_id"] == invoice["id"]), None)

    response = client.delete(f"/invoice-items/{item['id']}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "Invoice item deleted successfully"
