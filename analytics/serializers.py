from rest_framework import serializers
from .models import DailyEventsTable, EventTotal


class EventDailyRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyEventsTable
        fields = "__all__"


class EventTotalRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTotal
        fields = "__all__"
