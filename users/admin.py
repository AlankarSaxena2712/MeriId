from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import *

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "username",
                "password",
                "phone_number",
            ),
        }),
    )
    

admin.site.register(AadharCard)
