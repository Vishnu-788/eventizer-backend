from rest_framework import serializers

from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='booking.user.username', read_only=True)
    event_name = serializers.CharField(source='booking.event.e_title', read_only=True)
    event_starts = serializers.DateTimeField(source='booking.event.e_start_time', read_only=True)
    event_ends = serializers.DateTimeField(source='booking.event.e_end_time', read_only=True)
    seats = serializers.SerializerMethodField()
    class Meta:
        model = Ticket
        fields = [
            'id',
            'booking',
            'seats',
            'username',
            'event_name',
            'event_starts',
            'event_ends',
            'issued_at',
            'expires_at'
        ]
        read_only_fields = fields

    def get_seats(self, obj):
        return list(obj.seats.values_list("seat_no", flat=True))