import requests
from fastapi import HTTPException
from core import config

PAYPAL_BASE_URL = config.settings.PAYPAL_BASE_URL
PAYPAL_CLIENT_ID = config.settings.PAYPAL_CLIENT_ID
PAYPAL_SECRET = config.settings.PAYPAL_SECRET


def get_paypal_token():
    url = f"{PAYPAL_BASE_URL}/v1/oauth2/token"
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    auth = (PAYPAL_CLIENT_ID, PAYPAL_SECRET)
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, auth=auth, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    raise HTTPException(status_code=400, detail="Failed to get PayPal token")


def create_order(access_token, order_data):
    url = f"{PAYPAL_BASE_URL}/v2/checkout/orders"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {access_token}"}
    response = requests.post(url, headers=headers, json=order_data)
    if response.status_code == 201:
        return response.json()
    raise HTTPException(
        status_code=400, detail="Failed to create PayPal order")


def capture_order(access_token, order_id):
    url = f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {access_token}"}
    response = requests.post(url, headers=headers)
    if response.status_code == 201:
        return response.json()
    raise HTTPException(
        status_code=400, detail="Failed to capture PayPal order")
