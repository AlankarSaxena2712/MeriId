from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from users.models import *

from rest_framework.authtoken.models import Token 

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "username",
                "password",
                "phone_number",
                "name",
                "status",
                "kyc_status",
                "aadhar_limit",
                "profile",
                "role",
                "address",
            ),
        }),
    )
    

admin.site.register(Kyc)
admin.site.register(Token)
admin.site.register(Address)

admin.site.unregister(Group)
