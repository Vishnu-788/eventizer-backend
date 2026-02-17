from django.db import transaction
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
from bookings.serializers import BookingCreateSerializer
from events.models import Seat


"""
Creates the booking entry with status 'PENDING'
Returns the booking instance with id attached to it.
Client makes another http request to payment app to initiate the payment.
"""
class BookingCreateView(CreateAPIView):
    serializer_class = BookingCreateSerializer
    def perform_create(self, serializer):
        seat_ids = self.request.data.get("seats")
        with transaction.atomic():
            seats = Seat.objects.select_for_update().filter(id__in=seat_ids)
            serializer.save(user=self.request.user)


