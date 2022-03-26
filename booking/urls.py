from django.urls import path

from users.views import *

urlpatterns = [
    path("booking", AddOperator.as_view(), name="booking"),
]
