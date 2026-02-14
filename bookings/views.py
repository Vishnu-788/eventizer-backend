from django.db import transaction
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from bookings.serializers import BookingCreateSerializer
from events.models import Seat


# Create your views here.
class BookingCreateView(CreateAPIView):
    serializer_class = BookingCreateSerializer
    def perform_create(self, serializer):
        seat_ids = self.request.data.get("seats")

        with transaction.atomic():
            # Lock seats
            seats = Seat.objects.select_for_update().filter(id__in=seat_ids)
            serializer.save(user=self.request.user)
