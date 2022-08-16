from django.urls import path

from  booking.views import *

urlpatterns = [
    path("booking", BookingView.as_view(), name="booking"),
    path("booking/location/<str:booking_uuid>", OperatorBookingLocationView.as_view(), name="booking_location"),
]
