from django.db import models

from bookings.models import Bookings
from events.models import Seat


# Create your models here.
class Ticket(models.Model):
    booking = models.OneToOneField(Bookings, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)