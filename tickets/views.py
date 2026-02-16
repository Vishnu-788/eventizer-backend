from django.shortcuts import render
from rest_framework.generics import ListAPIView

from tickets.models import Ticket
from tickets.serializers import TicketSerializer


# Create your views here.
class TicketListView(ListAPIView):
    serializer_class = TicketSerializer
    def get_queryset(self):
        return (
            Ticket.objects
            .filter(booking__user=self.request.user)
            .select_related("booking", "booking__event", "booking__user")
            .prefetch_related("seats")
        )


