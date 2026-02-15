from django.urls import path

from payments.views import PaymentCreateView, PayPalWebHook

urlpatterns = [
    path('<int:booking_id>/booking/', PaymentCreateView.as_view(), name='payment_create'),
    path('paypal/webhook/', PayPalWebHook.as_view(), name='paypal_webhook'),
]