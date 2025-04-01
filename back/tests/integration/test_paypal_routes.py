from unittest.mock import patch


def test_test_paypal_token(client):
    with patch("external.paypal_client.get_paypal_token", return_value="fake-token"):
        response = client.get("/client/test-paypal-token")
        assert response.status_code == 200
        assert response.json() == {"token": "fake-token"}


def test_create_paypal_order(client, auth_header, sample_cart_item):
    with patch("services.paypal_service.paypal_client.get_paypal_token", return_value="fake-token"), \
            patch("services.paypal_service.paypal_client.create_order", return_value={"id": "ORDER123"}):
        response = client.post(
            "/client/create-paypal-order", headers=auth_header)
        assert response.status_code == 201
        assert response.json()["id"] == "ORDER123"


def test_capture_paypal_order(client, auth_header, sample_cart_item):
    with patch("services.paypal_service.paypal_client.get_paypal_token", return_value="fake-token"), \
            patch("services.paypal_service.paypal_client.capture_order", return_value={"id": "CAPTURE123", "status": "COMPLETED"}):
        response = client.post(
            "/client/capture-paypal-order/ORDER123", headers=auth_header)
        assert response.status_code == 200
        assert "invoice_id" in response.json()
