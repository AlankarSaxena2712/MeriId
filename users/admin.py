from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import messages

from users.models import *

from rest_framework.authtoken.models import Token 


class KycVerificationAdmin(admin.AdminSite):
    site_header = "KYC Verification"
    site_title = "KYC Verfication Admin Portal"
    index_title = "Welcome to KYC Verification Admin Portal"

    def has_permission(self, request):
        if request.user.is_active and request.user.role == "kyc_verifier":
            return True
        return False


kyc_verification_admin_site = KycVerificationAdmin(name="user_support_admin")


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
                "gender",
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
        ('Permissions', {
            "classes": ["collapse",],
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
        }),
    )
    readonly_fields = ("uuid",)


class KYCAdmin(admin.ModelAdmin):
    list_display = ['id', "name", "user_journey", "created_at", "updated_at", "verified"]
    list_display_links = ["id", "name", "user_journey"]
    fieldsets = (
        (None, {
            "fields": (
                "user",
                "name",
                "user_journey"
            ),
        }),
        ("Aadhar Details", {
            "fields": ("aadhar_card","aadhar_card_image",),
        }),
        ("Pan Details", {
            "fields": ("pan_card","pan_card_image",),
        }),
        ("Other Documents Details", {
            "fields": ("other_documents","other_document_image",),
        }),
        ("Video Details", {
            "fields": ("video_link","video_preview",),
        }),
        ("Verification", {
            "fields": ("verified",),
        }),
    )
    readonly_fields = ["name", "user_journey", "aadhar_card_image", "pan_card_image", "other_document_image", "video_preview"] 
    list_filter = ["verified"]


admin.site.register(Kyc)
# admin.site.register(Token)
admin.site.register(Address)
admin.site.register(Attendance)
admin.site.register(Issue)
admin.site.register(PinCode)

# admin.site.unregister(Group)

kyc_verification_admin_site.register(Kyc, KYCAdmin)

