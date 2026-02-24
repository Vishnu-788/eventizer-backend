from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auth_user.enums import UserRoles
from auth_user.models import User

def username_field():
    return serializers.RegexField(
        regex=r'^[a-zA-Z0-9_]{3,20}$',
        validators=[UniqueValidator(queryset=User.objects.all())],
        error_messages={
            "invalid": "Username must be 3–20 characters and contain only letters, numbers, or underscores."
        }
    )

def email_field():
    return serializers.EmailField(
        allow_null=False,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['role'] = self.user.role
        data['verified'] = self.user.verified
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        return data


# I will later convert this into ModelSerializer for more readability.
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = username_field()
    email = email_field()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserRoles.choices, default=UserRoles.USER)
    verified = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        password = validated_data.pop('password')
        if validated_data['role'] == UserRoles.HOST:
            # This condition is here to ensure that the user can only send host or user as the role in Json body.
            pass
        else:
            validated_data['role'] = UserRoles.USER
            validated_data['verified'] = True

        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

class UserRetrieveUpdateSerializer(serializers.Serializer):
    username = username_field()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = email_field()
    role = serializers.ChoiceField(choices=UserRoles.choices, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    verified = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance






