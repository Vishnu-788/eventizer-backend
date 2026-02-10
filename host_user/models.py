from django.db import models
from auth_user.models import User
from .enums import Status

# Create your models here.
class Host(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    company_name = models.CharField(max_length=100)
    company_contact_no = models.IntegerField(null=False)
    company_contact_email = models.EmailField(null=False)
    status = models.CharField(
        max_length=10,
        choices=Status,
        default=Status.PENDING
    )

