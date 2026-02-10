# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

"""
To view the extra fields mentioned in the CustomUser in the admin panel.
"""
@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {
            "fields": ("verified", "role"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Fields", {
            "fields": ("verified", "role"),
        }),
    )
