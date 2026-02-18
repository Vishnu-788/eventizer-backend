from datetime import timedelta, datetime
from django.utils import timezone

from rest_framework import serializers
from host_user.models import Host
from .models import Event, Seat

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'e_title', 'e_date', 'e_start_time', 'e_category', 'price', 'e_venue']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields=('id', 'host')

    def validate(self, data):
        e_date = data.get('e_date')
        start = data.get('e_start_time')
        end = data.get('e_end_time')

        today = timezone.now()
        min_interval_date = today + timedelta(days=5)
        e_date = datetime.combine(e_date, datetime.min.time())

        # if e_date <  min_interval_date:
        #     raise serializers.ValidationError({
        #         'detail': "Event data should be scheduled before 5 days at least."
        #     })
        #
        #
        # if e_date < today:
        #     raise serializers.ValidationError({
        #         'detail': "Event date is in past. Invalid date"
        #     })

        if start and end:
            start_dt = datetime.combine(today, start)
            end_dt = datetime.combine(today, end)

            diff = end_dt - start_dt

            if diff.total_seconds() < 3600:
                raise serializers.ValidationError({
                    "e_end_time": "Event duration must be at least 1 hour."
                })

            if end <= start:
                raise serializers.ValidationError({
                    "e_end_time": "End time must be after start time."
                })
        return data


"""
Return the details of the host along with the event details.
"""
class HostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ['company_name', 'company_contact_no', 'company_contact_email']

class EventDetailSerializer(serializers.ModelSerializer):
    host = HostViewSerializer(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_no', 'booked']