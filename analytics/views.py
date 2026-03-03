from rest_framework.generics import ListAPIView
from auth_user.permissions import IsVerifiedHost
from .models import DailyEventsTable, EventTotal
from .serializers import EventDailyRevenueSerializer, EventTotalRevenueSerializer


# Create your views here.
class EventDailyRevenueAnalyticsView(ListAPIView):
    permission_classes = [IsVerifiedHost]
    serializer_class = EventDailyRevenueSerializer
    lookup_url_kwarg = "event_id"

    def get_queryset(self):
        event_id = self.kwargs.get(self.lookup_url_kwarg)
        return DailyEventsTable.objects.filter(event_id=event_id)


class EventTotalRevenueAnalyticsView(ListAPIView):
    permission_classes = [IsVerifiedHost]
    serializer_class = EventTotalRevenueSerializer
    lookup_url_kwarg = "event_id"

    def get_queryset(self):
        event_id = self.kwargs.get(self.lookup_url_kwarg)
        return EventTotal.objects.filter(event_id=event_id)
