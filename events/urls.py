from django.urls import path
from events.views import EventCRUDView, EventListView

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('host/', EventCRUDView.as_view(), name='event_crud'),
]