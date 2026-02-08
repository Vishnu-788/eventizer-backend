from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from auth_user.enums import UserRoles
from auth_user.models import User

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
    password = serializers.CharField(allow_null=False)
    role = serializers.ChoiceField(choices=UserRoles.choices, default=UserRoles.USER)
    verified = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        if validated_data['role'] == UserRoles.USER:
            validated_data['verified'] = True
            validated_data['username'] = validated_data['username'].lower()
        return User.objects.create(**validated_data)
