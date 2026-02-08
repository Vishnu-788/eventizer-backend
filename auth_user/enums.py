from django.db import models

class UserRoles(models.TextChoices):
    ADMIN = ('admin', 'Admin')
    USER = ('user', 'User')
    HOST = ('host', 'Host')

