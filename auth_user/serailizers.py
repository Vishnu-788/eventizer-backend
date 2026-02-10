from typing import Any

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auth_user.enums import UserRoles
from auth_user.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['role'] = self.user.role
        data['verified'] = self.user.verified
        return data


# I will later convert this into ModelSerializer for more readability.
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.RegexField(
        regex=r'^[a-zA-Z0-9_]{3,20}$',
        validators=[UniqueValidator(queryset=User.objects.all())],
        error_messages={
            "invalid": "Username must be 3–20 characters and contain only letters, numbers, or underscores."
        }
    )
    email = serializers.EmailField(
        allow_null=False,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserRoles.choices, default=UserRoles.USER)
    verified = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        password = validated_data.pop('password')
        if validated_data['role'] == UserRoles.HOST:
            # This condition is here to ensure that the user can only send host or user as the json in body.
            pass
        else:
            validated_data['role'] = UserRoles.USER
            validated_data['verified'] = True

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


