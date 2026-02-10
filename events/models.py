from django.db import models

from host_user.models import Host


# Create your models here.
class Event(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, null=False, blank=False)
    e_title = models.CharField(max_length=100, null=False, blank=False)
    e_description = models.TextField(max_length=500)
    e_venue = models.CharField(max_length=100, null=False, blank=False)
    e_date_time = models.DateTimeField(null=False, blank=False)
    e_category = models.CharField(max_length=100, null=False, blank=False)
    total_seats = models.IntegerField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    
