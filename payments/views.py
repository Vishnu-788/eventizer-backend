from typing import Any

from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404, CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json
from bookings.models import Bookings
from payments.serializers import PaymentCreateSerializer
from bookings.enums import BookingStatus
from .models import Payment
from .services import create_paypal_order

"""
Receives the booking id from the url. Post body is empty dont accept anything.
get the booking with the booking id.
populate the payment object.
booking -> get booking with id.
amount -> booking.amount.
status -> give none since default is Created.
user -> current authenticated user
"""
class PaymentCreateView(CreateAPIView):
    serializer_class = PaymentCreateSerializer
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.approval_url = None

    def get_booking(self):
        return get_object_or_404(
            Bookings,
            pk=self.kwargs['booking_id'],
            user=self.request.user,
            booking_status=BookingStatus.PENDING
        )

    def perform_create(self, serializer):
        booking = self.get_booking()
        existing = Payment.objects.filter(booking=booking, status__in=[BookingStatus.PENDING]).first()
        if existing:
            raise ValidationError("Payment already initiated")

        payment = serializer.save(
            booking=booking,
            user=self.request.user,
            amount=booking.total_amount
        )

        paypal_order_id, approval_url = create_paypal_order(payment)
        payment.paypal_order_id = paypal_order_id
        payment.save(update_fields=["paypal_order_id"])
        self.approval_url = approval_url

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'approval_url': self.approval_url}, status=status.HTTP_201_CREATED)

"""
Paypal will ping this endpoint to let the server know about the payment status.
"""
class PayPalWebHook(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        print("\n====== PAYPAL WEBHOOK ======")
        print(json.dumps(request.data, indent=2))
        print("====== END ======\n")

        return HttpResponse(status=200)




