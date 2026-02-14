from django.db import models

class Status(models.TextChoices):
    CREATED='created'
    PENDING='pending'
    APPROVED='approved'
    REJECTED='rejected'