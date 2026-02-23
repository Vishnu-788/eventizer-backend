from django.db import transaction
from django.db.models.aggregates import Count
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from auth_user.permissions import IsVerifiedHost
from bookings.serializers import BookingCreateSerializer, BookingEventListSerializer, BookingUserListSerializer
from events.models import Seat
from .models import Bookings


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

class BookingUserListView(ListAPIView):
    permission_classes = {IsAuthenticated}
    serializer_class = BookingUserListSerializer
    def get_queryset(self):
        return (
            Bookings.objects
                .filter(user=self.request.user)
                .select_related("event", "user")
                .annotate(seat_count=Count("seats"))
        )

"""
Return the bookings of a particular event.
event id received from the url parameter.
returns the list of booking for that particular event.
"""
class BookingListView(ListAPIView):
    permission_classes = [IsVerifiedHost]
    serializer_class = BookingEventListSerializer
    lookup_url_kwarg = 'event_id'
    def get_queryset(self):
        return Bookings.objects.filter(event=self.kwargs['event_id'])



