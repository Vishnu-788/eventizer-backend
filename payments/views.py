from typing import Any
import json
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    get_object_or_404,
    CreateAPIView,
    GenericAPIView,
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from bookings.models import Bookings
from bookings.enums import BookingStatus
from .serializers import (
    PaymentCreateSerializer,
    PaymentStatusPollSerializer,
    PaymentListSerializer,
)
from .models import Payment
from .services import (
    create_paypal_order,
    handle_checkout_approved,
    handle_capture_completed,
    handle_payment_failed,
)
from auth_user.enums import UserRoles

"""
Receives the booking id from the url. CHeck if a booking exists with that id and check its status. 
If booking exists check it booking status field. if its 'PENDING' -> 
    Create a payment entry and attach the payment entry and put it
    as the reference id in the paypal_order.
    Returns an approval url where USER can click the buy button.
If the booking doesn't exists or the status is anything other than pending. 
    Dont initiate the payment return an error with appropriate error message.

"""


class PaymentCreateView(CreateAPIView):
    serializer_class = PaymentCreateSerializer

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.approval_url = None

    def get_booking(self):
        return get_object_or_404(
            Bookings,
            pk=self.kwargs["booking_id"],
            user=self.request.user,
            booking_status=BookingStatus.PENDING,
        )

    def validate_booking_state(self, booking):
        if booking.booking_status == BookingStatus.PENDING:
            return None

        messages = {
            BookingStatus.APPROVED: ("Payment is processing.", 409),
            BookingStatus.CANCELLED: ("Payment Cancelled.", 402),
            BookingStatus.BOOKED: ("Already paid.", 409),
        }

        msg, code = messages.get(
            booking.booking_status, ("Invalid booking state.", 400)
        )
        return Response({"detail": msg}, status=code)

    def perform_create(self, serializer):
        booking = self.get_booking()
        existing = Payment.objects.filter(
            booking=booking, status__in=[BookingStatus.PENDING]
        ).first()
        if existing:
            raise ValidationError("Payment already initiated")

        payment = serializer.save(
            booking=booking, user=self.request.user, amount=booking.total_amount
        )

        paypal_order_id, approval_url = create_paypal_order(payment)
        payment.paypal_order_id = paypal_order_id
        payment.save(update_fields=["paypal_order_id"])
        self.approval_url = approval_url

    def create(self, request, *args, **kwargs):
        booking = self.get_booking()
        error = self.validate_booking_state(booking)
        if error:
            return error
        super().create(request, *args, **kwargs)
        return Response(
            {"approval_url": self.approval_url}, status=status.HTTP_201_CREATED
        )


"""
Paypal will ping this endpoint to let the server know about the payment status.
"""


class PayPalWebHook(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        event = request.data
        event_type = event.get("event_type")

        if event_type == "CHECKOUT.ORDER.APPROVED":
            handle_checkout_approved(event)

        elif event_type == "PAYMENT.CAPTURE.COMPLETED":
            handle_capture_completed(event)

        elif event_type == "PAYMENT.CAPTURE.FAILED":
            handle_payment_failed(event)
        return HttpResponse(status=200)


class UserPaymentListView(ListAPIView):
    serializer_class = PaymentListSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class PaymentStatusPollingView(RetrieveAPIView):
    queryset = Payment.objects.all()
    lookup_field = "paypal_order_id"
    lookup_url_kwarg = "order_id"
    serializer_class = PaymentStatusPollSerializer
