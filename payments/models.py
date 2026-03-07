from django.db import models
from auth_user.models import User
from events.models import Event
from bookings.models import Bookings
from .enums import Status

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=Status,
        default=Status.CREATED,
    )
    paypal_order_id = models.CharField(max_length=255, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

