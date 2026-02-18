from django.urls import path

from payments.views import PaymentCreateView, PayPalWebHook, PaymentStatusPollingView, UserPaymentListView

urlpatterns = [
    path('<int:booking_id>/booking/', PaymentCreateView.as_view(), name='payment_create'),
    path('paypal/webhook/', PayPalWebHook.as_view(), name='paypal_webhook'),
    path('status/<str:order_id>/', PaymentStatusPollingView.as_view(), name='payment_status'),
    path('user/list/', UserPaymentListView.as_view(), name='user_payment_list'),
]