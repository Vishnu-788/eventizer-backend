from django.urls import path

from bookings.views import BookingCreateView, BookingListView, BookingUserListView

urlpatterns = [
    path('', BookingCreateView.as_view(), name='create_booking'),
    path('user/list/', BookingUserListView.as_view(), name='list_bookings'),
    path('host/view-booking/<int:event_id>/', BookingListView.as_view(), name='view_booking'),
]