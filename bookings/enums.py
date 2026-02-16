from django.db import models

class BookingStatus(models.TextChoices):
    APPROVED = 'approved'
    PENDING = 'pending'
    BOOKED = 'booked'
    CANCELLED = 'cancelled'