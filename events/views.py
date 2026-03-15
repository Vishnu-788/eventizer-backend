from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
    CreateAPIView,
)

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.request import Request

from auth_user.permissions import IsVerifiedHost
from llm_rag.tasks import create_embeddings

from .models import Event, Seat
from .serializers import (
    EventSerializer,
    EventDetailSerializer,
    SeatSerializer,
    EventListSerializer,
)

from core.exceptions import VectorDbUnavailableException
from django.db import transaction


class HostEventListView(ListAPIView):
    permission_classes = [IsVerifiedHost]
    serializer_class = EventListSerializer

    def get_queryset(self):
        return Event.objects.filter(host=self.request.user.host)


class HostEventCreateView(CreateAPIView):
    permission_classes = [IsVerifiedHost]
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        host = self.request.user.host
        event = serializer.save(host=host)
        transaction.on_commit(lambda: create_embeddings.delay(event.id))


class HostEventDetailView(RetrieveAPIView):
    serializer_class = EventDetailSerializer
    permission_classes = [IsVerifiedHost]
    lookup_field = "id"

    def get_queryset(self):
        return Event.objects.filter(host=self.request.user.host)


"""
For users, list all the events available on the platform.
"""


class EventListView(ListAPIView):
    serializer_class = EventListSerializer

    def get_queryset(self):
        return Event.objects.filter(e_date__gte=timezone.now().date()).order_by(
            "e_date", "e_start_time"
        )


class EventDetailView(RetrieveAPIView):
    queryset = Event.objects.select_related("host")
    serializer_class = EventDetailSerializer
    lookup_field = "id"


class SeatListView(ListAPIView):
    serializer_class = SeatSerializer

    def get_queryset(self):
        event_id = str(self.kwargs["event_id"])
        return Seat.objects.filter(event=event_id)

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        event = get_object_or_404(Event, pk=kwargs["event_id"])

        return Response(
            {"event_price": event.price, "seats": serializer.data},
            status=status.HTTP_200_OK,
        )
