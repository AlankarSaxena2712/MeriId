from django.contrib import admin
from booking.models import *
# Register your models here. 

class BookingAdmin(admin.ModelAdmin):
    list_display = ["booking_id", "user", "slot_date", "slot_time", "booking_status", "operator"]
    list_display_links = ["booking_id"]
    ordering = ["slot_date", "booking_id"]

admin.site.register(Booking, BookingAdmin)
admin.site.register(Friend)
admin.site.register(Order)