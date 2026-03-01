from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .enums import BookingStatus

from events.models import Seat
from .models import Bookings

class BookingCreateSerializer(serializers.ModelSerializer):
    seats = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(),
        many=True,
    )
    class Meta:
        model = Bookings
        fields = ['id', 'user', 'event', 'seats', 'total_amount', 'booking_status']
        read_only_fields = ['user', 'total_amount', 'booking_status']

    def validate(self, data):
        event = data.get('event')
        seats = data.get('seats')
        if not seats:
            raise ValidationError('At least one seat is required')

        for seat in seats:
            if seat.event != event:
                raise ValidationError('Seat is not available for this event')
            if seat.booked:
                raise ValidationError('Seat already booked')
        return data

    def create(self, validated_data: dict) -> Bookings:
        validated_data['total_amount'] = validated_data['event'].price * len(validated_data['seats'])
        seats = validated_data.pop('seats')
        booking = Bookings.objects.create(**validated_data, booking_status=BookingStatus.PENDING)
        booking.seats.set(seats)
        return booking

class BookingUserListSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.e_title', read_only=True)
    seat_count = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Bookings
        fields = ['id', 'username', 'email', 'event_name', 'total_amount', 'booking_status', 'seat_count']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_no']

class BookingEventListSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model=Bookings
        fields='__all__'


