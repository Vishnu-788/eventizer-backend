from django.db import models

class Status(models.TextChoices):
    APPROVED = 'approved'
    PENDING = 'pending'
    REJECTED = 'rejected'