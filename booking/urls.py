from django.urls import path

from  booking.views import *

urlpatterns = [
    path("booking", BookingView.as_view(), name="booking"),
    path("booking/location/<str:booking_uuid>", OperatorBookingLocationView.as_view(), name="booking_location"),
    path("order/send-otp", OrderOtpSendAPI.as_view(), name="order_otp_send"),
    path("order/verify-otp", OrderOtpVerifyAPI.as_view(), name="order_otp_verify"),
    path("booking/admin", AdminWiseBookingList.as_view(), name="booking_admin"),
    path("booking/admin/changes", AdminWiseBookingUpdateApi.as_view(), name="booking_admin_changes"),
    path("booking/operator-slot", BookingOperatorSlot.as_view(), name="booking_operator_slot"),
]
