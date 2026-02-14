from django.db import models
from auth_user.models import User
from events.models import Event, Seat
from .enums import BookingStatus
from payments.models import Payment

# Create your models here.
class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, null=True)
    seats = models.ManyToManyField(Seat)
    total_amount = models.FloatField(null=False, blank=False)
    booking_status = models.CharField(
        max_length=20,
        choices=BookingStatus,
        default=BookingStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



