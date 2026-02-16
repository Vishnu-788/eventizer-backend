from django.urls import path

from tickets.views import TicketListView

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket_list'),
]