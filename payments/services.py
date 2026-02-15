import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


def get_paypal_token():
    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"

    response = requests.post(
        url,
        auth=HTTPBasicAuth(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
        },
        data={
            "grant_type": "client_credentials"
        }
    )
    response.raise_for_status()
    return response.json()["access_token"]


def create_paypal_order(payment):
    token = get_paypal_token()

    url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    body = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "reference_id": str(payment.id),
                "amount": {
                    "currency_code": "USD",
                    "value": str(payment.amount)
                }
            }
        ],
        "application_context": {
            "return_url": "http://localhost:4200/payment/success",
            "cancel_url": "http://localhost:4200/payment/cancel"
        }
    }

    res = requests.post(url, json=body, headers=headers)
    data = res.json()

    print("ORDER STATUS:", res.status_code)
    print("ORDER BODY:", data)

    res.raise_for_status()

    approval_url = next(link["href"] for link in data["links"] if link["rel"] == "approve")
    if res.status_code != 201:
        print("PAYPAL ERROR:", res.text)
        raise Exception("Order creation failed")

    return data["id"], approval_url

