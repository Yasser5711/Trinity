from unittest.mock import patch

import pytest

import services.paypal_service as paypal_service
from tests.factories import CartFactory, CartItemFactory, ProductFactory, StockFactory


@pytest.mark.skip(reason="Skipping this test temporarily")
def test_create_paypal_order_success(db_session, sample_user):
    product = ProductFactory(price=10.0)
    stock = StockFactory(product=product, quantity=20)
    cart = CartFactory(user_id=sample_user.id, status="PENDING")
    db_session.add(stock)

    item = CartItemFactory(product=product, cart=cart, quantity=2)
    db_session.add_all([cart, item])
    db_session.commit()
    db_session.refresh(cart)
    db_session.refresh(item)
    assert cart.items is not None and len(cart.items) > 0, "Cart items not loaded"
    with (
        patch(
            "services.paypal_service.paypal_client.get_paypal_token",
            return_value="fake-token",
        ),
        patch(
            "services.paypal_service.paypal_client.create_order",
            return_value={"id": "fake-order"},
        ),
    ):
        result = paypal_service.create_paypal_order(db_session, sample_user.id)

        assert result["id"] == "fake-order"


@pytest.mark.skip(reason="Skipping this test temporarily")
def test_capture_paypal_order_success(db_session):
    product = ProductFactory(price=10.0)
    StockFactory(product=product, quantity=20)
    cart = CartFactory(user_id=2)

    item = CartItemFactory(product=product, cart=cart, quantity=2)
    db_session.add_all([cart, item])
    db_session.commit()
    db_session.refresh(cart)
    db_session.refresh(item)

    assert cart.items is not None and len(cart.items) > 0, "Cart items not loaded"
    with (
        patch(
            "services.paypal_service.paypal_client.get_paypal_token",
            return_value="fake-token",
        ),
        patch(
            "services.paypal_service.paypal_client.capture_order",
            return_value={"id": "CAPTURE123", "status": "COMPLETED"},
        ),
    ):
        result = paypal_service.capture_paypal_order(db_session, 2, "ORDER123")
        assert result["message"] == "Order successfully captured and processed"
