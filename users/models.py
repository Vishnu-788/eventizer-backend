from django.contrib.auth.models import AbstractUser
from django.db import models
from .enums import UserRoles

# Create your models here.
class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.USER
    )
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
