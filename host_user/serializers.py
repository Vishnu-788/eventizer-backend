from rest_framework import serializers
from .models import Host

"""
Serializer is for performing CRUD operations by the user.role == host.
All the other fields except id, user, status of the current authenticated host 
are editable by the current authenticated host.
"""
class HostCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model=Host
        fields=['user', 'company_name', 'company_contact_no', 'company_contact_email', 'status']
        read_only_fields=['user', 'status']

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