from django.db import models
from events.models import Event

# Create your models here.
class DailyEventsTable(models.Model):
    date = models.DateField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seats_sold = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "date"], name="unique_event_day")
        ]

class EventTotal(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    total_seats_sold = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_booking_at = models.DateTimeField()
