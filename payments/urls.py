from django.urls import path

from payments.views import PaymentCreateView

urlpatterns = [
    path('<int:booking_id>/booking/', PaymentCreateView.as_view(), name='payment_create'),
]