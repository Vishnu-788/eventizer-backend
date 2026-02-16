from decimal import Decimal

import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from datetime import datetime
from bookings.models import Bookings
from payments.models import Payment
from tickets.models import Ticket
from .enums import Status
from bookings.enums import BookingStatus


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
            "return_url": "http://localhost:4200/payment/processing",
            "cancel_url": "http://localhost:4200/payment/cancel"
        }
    }

    res = requests.post(url, json=body, headers=headers)
    data = res.json()

    res.raise_for_status()

    approval_url = next(link["href"] for link in data["links"] if link["rel"] == "approve")
    if res.status_code != 201:
        print("PAYPAL ERROR:", res.text)
        raise Exception("Order creation failed")

    return data["id"], approval_url

def capture_paypal_order(paypal_order_id):
    access_token = get_paypal_token()
    url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{paypal_order_id}/capture"
    requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
    )

def handle_checkout_approved(event):
    resource = event["resource"]
    paypal_order_id = resource["id"]

    payment_id = resource["purchase_units"][0]["reference_id"]
    payment = Payment.objects.get(id=payment_id)
    if payment.status != Status.PENDING:
        return
    payment.paypal_order_id = paypal_order_id
    payment.status = Status.APPROVED
    payment.save(update_fields=["paypal_order_id", "status"])
    capture_paypal_order(paypal_order_id)

def handle_capture_completed(event):
    paypal_order_id = event["resource"]["supplementary_data"]["related_ids"]["order_id"]
    amount_str = event["resource"]["amount"]["value"]
    amount = Decimal(amount_str)
    payment = Payment.objects.get(paypal_order_id=paypal_order_id)
    if payment.status != Status.APPROVED:
        return
    payment.status = Status.COMPLETED
    payment.amount = amount
    payment.save(update_fields=["amount", "status"])
    update_bookings_table(payment.booking, amount)

def update_bookings_table(booking: Bookings, amount):
    booking.booking_status = BookingStatus.BOOKED
    booking.seats.update(booked=True)
    booking.save(update_fields=["booking_status"])
    generate_ticket(booking, amount)

def generate_ticket(booking: Bookings, amount):
    event = booking.event
    expires = datetime.combine(event.e_date, event.e_end_time)
    ticket = Ticket.objects.create(
        booking=booking,
        amount=amount,
        expires_at=expires
    )
    ticket.seats.set(booking.seats.all())

def handle_payment_failed(event):
    order_id = event["resource"]["supplementary_data"]["related_ids"]["order_id"]
    payment = Payment.objects.select_related("booking").get(paypal_order_id=order_id)
    booking = payment.booking
    if payment.status in (Status.REJECTED, Status.COMPLETED):
        return
    payment.status=Status.REJECTED
    booking.booking_status=BookingStatus.CANCELLED
    payment.save(update_fields=["status"])
    booking.save(update_fields=["booking_status"])



