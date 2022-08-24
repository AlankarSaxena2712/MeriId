from django.urls import path

from  booking.views import *

urlpatterns = [
    path("booking", BookingView.as_view(), name="booking"),
    path("booking/location/<str:booking_uuid>", OperatorBookingLocationView.as_view(), name="booking_location"),
    path("order/send-otp", OrderOtpSendAPI.as_view(), name="order_otp_send"),
    path("order/verify-otp", OrderOtpVerifyAPI.as_view(), name="order_otp_verify"),
    path("booking/admin", AdminWiseBookingList.as_view(), name="booking_admin"),
    path("booking/admin/changes", AdminWiseBookingUpdateApi.as_view(), name="booking_admin_changes"),
    path("booking/operator-slot/<str:uuid>", BookingOperatorSlot.as_view(), name="booking_operator_slot"),
    path('list/operator', OperatorWiseBooking.as_view(), name='operator_wise_booking'),
    path("status/update", BookingStatusUpdateByOperatorAPI.as_view(), name="booking_status_update"),
    path("operator/verify", CreateHashedWebLinkForOperator.as_view(), name="operator-verify"),
]
