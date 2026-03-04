from django.urls import path
from .views import (
    EventDailyRevenueAnalyticsView,
    EventTotalRevenueAnalyticsView,
    EventDetailRevenueAnalyitcs,
)

urlpatterns = [
    path(
        "daily/<int:event_id>/event/",
        EventDailyRevenueAnalyticsView.as_view(),
        name="event_daily_analytics",
    ),
    path(
        "total/<int:event_id>/event/",
        EventTotalRevenueAnalyticsView.as_view(),
        name="event_total_analytics",
    ),
    path(
        "event/<int:event_id>/detail/",
        EventDetailRevenueAnalyitcs.as_view(),
        name="event_detail_analytics",
    ),
]
