from rest_framework import serializers

from auth_user.serailizers import UserRetrieveUpdateSerializer
from .models import Host

class HostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Host
        fields=['user', 'company_name', 'company_contact_no', 'company_contact_email', 'status']
        read_only_fields=['user', 'status']

"""
For update and detailed view of the verified host.
"""
class HostSerializer(serializers.ModelSerializer):
    user = UserRetrieveUpdateSerializer()
    class Meta:
        model=Host
        fields=['user', 'company_name', 'company_contact_email', 'company_contact_no', 'status']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if user_data:
            user = instance.user
            for attr, val in user_data.items():
                setattr(user, attr, val)
            user.save()
        return instance




"""
Serializer for user.role == admin. View all the hosts or based on the request params.
"""
class HostListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Host
        fields='__all__'

"""
Serializer is for user.role == admin only. For performing update on the 'status' field to verify the host.
This view will update the USER model's verified flag for completing the verification.
"""
class HostStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Host
        fields=['status']

    def update(self, instance, validated_data):
        new_status = validated_data.get('status', instance.status)
        instance.status = new_status

        if new_status == 'approved':
            instance.status = 'approved'
            instance.user.verified = True
            instance.user.save()
        else:
            instance.status = 'rejected'
        instance.save()
        return instance