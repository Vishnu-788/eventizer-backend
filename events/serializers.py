from rest_framework import serializers
from host_user.models import Host
from .models import Event, Seat

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'e_title', 'e_start_time', 'e_category', 'price', 'e_venue']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields=('id', 'host')

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