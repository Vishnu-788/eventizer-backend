from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
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


class EventDetailRevenueAnalyitcs(GenericAPIView):
    permission_classes = [IsVerifiedHost]

    def get(self, request, event_id):
        daily_revenue_data = DailyEventsTable.objects.filter(event_id=event_id)
        total_revenue_data = get_object_or_404(EventTotal, event_id=event_id)
        daily_serializer = EventDailyRevenueSerializer(daily_revenue_data, many=True)
        total_serializer = EventTotalRevenueSerializer(total_revenue_data)

        return Response(
            {"daily": daily_serializer.data, "total": total_serializer.data},
            status=status.HTTP_200_OK,
        )


class EventTotalRevenueAnalyticsView(RetrieveAPIView):
    permission_classes = [IsVerifiedHost]
    serializer_class = EventTotalRevenueSerializer
    lookup_field = "event_id"

    def get_queryset(self):
        return EventTotal.objects.filter(event_id=self.kwargs.get("event_id"))
