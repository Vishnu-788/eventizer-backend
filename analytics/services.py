from .models import DailyEventsTable
def update_daily_events_table(booking):
    event_entry = DailyEventsTable.objects.get_or_create(event=booking.event, date=)