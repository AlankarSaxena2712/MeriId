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
                "user_id",
                "uuid",
                "password",
                "email",
                "phone_number",
                "name",
                "status",
                "kyc_status",
                "aadhar_limit",
                "profile",
                "role",
                "address",
                "pincodes",
            ),
        }),
    )
    readonly_fields = ("uuid",)
    

admin.site.register(Kyc)
admin.site.register(Token)
admin.site.register(Address)
admin.site.register(Attendance)
admin.site.register(Issue)
admin.site.register(PinCode)

admin.site.unregister(Group)
