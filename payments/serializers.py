from rest_framework import serializers
from .models import Payment

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'booking', 'amount', 'status']
        read_only_fields = ['id', 'user', 'booking', 'amount', 'status']

class PaymentStatusPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['status']

class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'