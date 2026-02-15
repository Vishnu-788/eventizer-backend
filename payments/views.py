from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404, CreateAPIView

from bookings.models import Bookings
from payments.serializers import PaymentCreateSerializer
from bookings.enums import BookingStatus
from .models import Payment

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
        return payment



