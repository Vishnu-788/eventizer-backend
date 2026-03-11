from datetime import timedelta
from django.utils import timezone

from rest_framework import serializers
from host_user.models import Host
from .models import Event, Seat


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "e_title",
            "e_date",
            "e_start_time",
            "e_end_time",
            "e_category",
            "price",
            "e_venue",
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ("id", "host")

    def validate(self, data):
        e_date = data.get("e_date")
        start = data.get("e_start_time")
        end = data.get("e_end_time")

        today = timezone.now().date()

        # Event must be at least 5 days from now
        if e_date < today + timedelta(days=5):
            raise serializers.ValidationError(
                "Event date must be at least 5 days from today."
            )

        # Start must be before end
        if start >= end:
            raise serializers.ValidationError(
                "Event start time must be before end time."
            )

        # Minimum duration 1 hour
        if (end - start) < timedelta(hours=1):
            raise serializers.ValidationError("Event duration must be at least 1 hour.")

        return data


class EventIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        field = ["id", "e_title"]


"""
Return the details of the host along with the event details.
"""


class HostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ["company_name", "company_contact_no", "company_contact_email"]


class EventDetailSerializer(serializers.ModelSerializer):
    host = HostViewSerializer(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "seat_no", "booked"]
