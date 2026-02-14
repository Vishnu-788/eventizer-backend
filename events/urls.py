from django.urls import path
from events.views import EventCRUDView, EventListView, EventDetailView

urlpatterns = [
    path('<int:id>/detail/', EventDetailView.as_view(), name='event_detail'),
    path('', EventListView.as_view(), name='event_list'),
    path('host/', EventCRUDView.as_view(), name='event_crud'),
]