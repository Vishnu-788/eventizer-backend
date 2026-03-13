from django.db import transaction
from django.db.models import F
from .models import DailyEventsTable, EventTotal
import logging

logger = logging.getLogger(__name__)


def update_analytics_table(booking, payment_date):
    with transaction.atomic():
        logger.debug("Starting analytics update for booking ID: %s", booking.id)
        update_daily_events_table(booking, payment_date)
        update_event_total_table(booking, payment_date)


def update_daily_events_table(booking, payment_date):
    logger.debug("Updating daily events table for booking ID: %s", booking.id)
    event_entry, created = DailyEventsTable.objects.get_or_create(
        event=booking.event, date=payment_date, defaults={"seats_sold": 0, "revenue": 0}
    )

    DailyEventsTable.objects.filter(pk=event_entry.pk).update(
        seats_sold=F("seats_sold") + booking.seats.count(),
        revenue=F("revenue") + booking.total_amount,
    )


def update_event_total_table(booking, payment_date):
    logger.debug("Updating event total table for booking ID: %s", booking.id)
    event_entry, created = EventTotal.objects.get_or_create(
        event=booking.event,
        defaults={
            "total_seats_sold": 0,
            "total_revenue": 0,
            "last_booking_at": payment_date,
        },
    )
    EventTotal.objects.filter(pk=event_entry.pk).update(
        total_seats_sold=F("total_seats_sold") + booking.seats.count(),
        total_revenue=F("total_revenue") + booking.total_amount,
        last_booking_at=payment_date,
    )
