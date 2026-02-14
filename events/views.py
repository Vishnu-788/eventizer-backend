from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request

from auth_user.permissions import IsVerifiedHost
from host_user.models import Host

from .models import Event, Seat
from .serializers import EventSerializer, EventDetailSerializer, SeatSerializer

"""
CRUD view for creating, reading, updating and deleting events. Accessible by verified hosts.
"""
class EventCRUDView(GenericAPIView):
    permission_classes = [IsVerifiedHost]
    serializer_class = EventSerializer

    def get_queryset(self) -> QuerySet[Event]:
        return Event.objects.filter(host=self.get_host())

    def get_object(self, **kwargs) -> Event:
        return Event.objects.filter(host=self.get_host(), pk=kwargs['id']).first()

    def get_host(self) -> Host:
        return Host.objects.get(user=self.request.user)

    def get(self, request: Request) -> Response:
        queryset: QuerySet = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(host=self.get_host())
        return Response(
            {'message': 'success'},
            status=status.HTTP_201_CREATED
        )

    def patch(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Successfully updated'},
            status=status.HTTP_200_OK
        )

    def delete(self, request: Request) -> Response:
        event: Event = self.get_object()
        event.delete()
        return Response(
            {'message': 'success'},
            status=status.HTTP_204_NO_CONTENT
        )

"""
For users, list all the events available on the platform.
"""
class EventListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailView(RetrieveAPIView):
    queryset = Event.objects.select_related('host')
    serializer_class = EventDetailSerializer
    lookup_field = 'id'

class SeatListView(ListAPIView):
    serializer_class = SeatSerializer

    def get_queryset(self):
        event_id = str(self.kwargs['event_id'])
        return Seat.objects.filter(event=event_id)

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        event = get_object_or_404(Event, pk=kwargs['event_id'])

        return Response({
            'event_price': event.price,
            'seats': serializer.data
        }, status=status.HTTP_200_OK)





