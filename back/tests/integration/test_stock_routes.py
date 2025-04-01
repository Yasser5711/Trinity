import pytest


def test_get_all_stocks(client, admin_auth_header, sample_stock):
    response = client.get("/stocks", headers=admin_auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(stock["id"] == sample_stock.id for stock in response.json())


def test_get_stock_by_id(client, admin_auth_header, sample_stock):
    response = client.get(
        f"/stocks/{sample_stock.id}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == sample_stock.id


def test_get_stock_by_id_not_found(client, admin_auth_header):
    response = client.get("/stocks/99999", headers=admin_auth_header)
    assert response.status_code == 404


def test_create_stock(client, admin_auth_header, sample_product):
    payload = {
        "product_id": sample_product.id,
        "quantity": 50
    }
    response = client.post("/stocks", json=payload, headers=admin_auth_header)
    assert response.status_code == 201
    assert response.json()["product_id"] == sample_product.id
    assert response.json()["quantity"] == 50


def test_update_stock(client, admin_auth_header, sample_stock):
    payload = {
        "quantity": 200
    }
    response = client.put(
        f"/stocks/{sample_stock.id}", json=payload, headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "Stock updated successfully"


def test_update_stock_not_found(client, admin_auth_header):
    payload = {
        "quantity": 100
    }
    response = client.put("/stocks/99999", json=payload,
                          headers=admin_auth_header)
    assert response.status_code == 404


def test_delete_stock(client, admin_auth_header, sample_stock):
    response = client.delete(
        f"/stocks/{sample_stock.id}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "Stock deleted successfully"


def test_delete_stock_not_found(client, admin_auth_header):
    response = client.delete("/stocks/99999", headers=admin_auth_header)
    assert response.status_code == 404
