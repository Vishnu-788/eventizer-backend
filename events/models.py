from django.db import models
from host_user.models import Host


# Create your models here.
class Event(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, null=False, blank=False)
    e_title = models.CharField(max_length=100, null=False, blank=False)
    e_description = models.TextField(max_length=3000)
    e_venue = models.CharField(max_length=100, null=False, blank=False)
    e_date = models.DateField(null=False, blank=False)
    e_start_time = models.TimeField(null=False, blank=False)
    e_end_time = models.TimeField()
    e_category = models.CharField(max_length=100, null=False, blank=False)
    total_seats = models.IntegerField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)

    """
    Pre-generate seats for a particular event whenever there is a new entry 
    on events table. (Not Update, only when there is a new entry).
    """

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            seats = [
                Seat(event=self, seat_no=i) for i in range(1, self.total_seats + 1)
            ]
            Seat.objects.bulk_create(seats)


class Seat(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="seats")
    seat_no = models.IntegerField(null=False, blank=False)
    booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ("event", "seat_no")
