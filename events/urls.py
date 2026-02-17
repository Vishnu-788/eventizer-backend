from django.urls import path
from events.views import EventCRUDView, EventListView, EventDetailView, SeatListView

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('<int:id>/detail/', EventDetailView.as_view(), name='event_detail'),
    path('host/', EventCRUDView.as_view(), name='event_crud'),
    path('seats/<int:event_id>/', SeatListView.as_view(), name='seat_list'),
]