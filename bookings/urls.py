from django.urls import path

from bookings.views import BookingCreateView, BookingListView

urlpatterns = [
    path('', BookingCreateView.as_view(), name='create_booking'),
    path('host/view-booking/<int:event_id>/', BookingListView.as_view(), name='view_booking'),
]