from django.contrib import admin

from events.models import Seat, Event

# Register your models here.
admin.site.register(Event)
admin.site.register(Seat)
