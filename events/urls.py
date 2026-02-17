from django.urls import path
from events.views import EventListView, EventDetailView, SeatListView, HostEventCreateView, HostEventListView, \
    HostEventDetailView

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('<int:id>/detail/', EventDetailView.as_view(), name='event_detail'),

    # Host related paths.
    path('host/create/', HostEventCreateView.as_view(), name='event_crud'),
    path('host/list/', HostEventListView.as_view(), name='event_list'),
    path('host/detail/<int:id>/', HostEventDetailView.as_view(), name='event_detail'),

    path('seats/<int:event_id>/', SeatListView.as_view(), name='seat_list'),
]