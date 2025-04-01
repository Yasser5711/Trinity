from datetime import datetime
from tests.factories import CartFactory, CartItemFactory, ProductFactory


def test_get_all_invoices(client, admin_auth_header):
    response = client.get("/invoices", headers=admin_auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_invoice_by_id(client, admin_auth_header, admin_user, sample_cart_item):
    product = ProductFactory()
    cart = CartFactory(user=admin_user)
    CartItemFactory(cart=cart, product=product, quantity=2)
    invoice_resp = client.post("/client/checkout", headers=admin_auth_header)
    print(invoice_resp.json())
    invoice_id = invoice_resp.json()["id"]

    response = client.get(f"/invoices/{invoice_id}", headers=admin_auth_header)

    assert response.status_code == 200
    assert response.json()["id"] == invoice_id


def test_create_invoice(client, admin_auth_header, sample_user, sample_product):
    payload = {
        "user_id": sample_user.id,
        "items": [
            {
                "product_id": sample_product.id,
                "quantity": 2,
                "price": 15.0
            }
        ]
    }
    response = client.post("/invoices", json=payload,
                           headers=admin_auth_header)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["total_amount"] == 30.0


def test_update_invoice(client, admin_auth_header, sample_user, sample_product):
    payload = {
        "user_id": sample_user.id,
        "items": [{"product_id": sample_product.id, "quantity": 1, "price": 10.0}]
    }
    invoice = client.post("/invoices", json=payload,
                          headers=admin_auth_header).json()

    update_payload = {
        "items": [{"product_id": sample_product.id, "quantity": 3, "price": 10.0}]
    }
    response = client.put(
        f"/invoices/{invoice['id']}", json=update_payload, headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "Invoice updated successfully"


def test_delete_invoice(client, admin_auth_header, sample_user, sample_product):
    payload = {
        "user_id": sample_user.id,
        "items": [{"product_id": sample_product.id, "quantity": 1, "price": 5.0}]
    }
    invoice = client.post("/invoices", json=payload,
                          headers=admin_auth_header).json()

    response = client.delete(
        f"/invoices/{invoice['id']}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "Invoice deleted successfully"


def test_get_yearly_sales(client, admin_auth_header):
    year = datetime.now().year
    response = client.get(
        f"/invoices/yearly-sales?year={year}", headers=admin_auth_header)
    assert response.status_code == 200
    assert "monthly_sales" in response.json()


def test_get_monthly_sales(client, admin_auth_header):
    now = datetime.now()
    response = client.get(
        f"/invoices/monthly-sales?year={now.year}&month={now.month}", headers=admin_auth_header
    )
    assert response.status_code == 200
    assert "total_sales" in response.json()


def test_checkout_fails_with_empty_cart(client, admin_auth_header):
    response = client.post("/client/checkout", headers=admin_auth_header)
    assert response.status_code == 400
    assert response.json()["detail"] == "Cart is empty"
