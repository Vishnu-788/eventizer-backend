from django.db import models

class BookingStatus(models.TextChoices):
    PENDING = 'pending'
    BOOKED = 'booked'
    CANCELLED = 'cancelled'