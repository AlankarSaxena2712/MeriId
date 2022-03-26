from django.urls import path

from  booking.views import *

urlpatterns = [
    path("booking", BookingView.as_view(), name="booking"),
]
