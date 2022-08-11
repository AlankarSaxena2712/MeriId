import uuid as uuid
from django.contrib.auth import get_user_model

from services.constants import BOOKING_STATUS


User = get_user_model()
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

# Create your models here.
class Booking(models.Model):
    """
    bookin model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User , related_name='friends')
    booking_time = models.DateTimeField(auto_now_add=True)
    preferred_slot_time = models.DateTimeField(null=True) 
    operator_arrival_time = models.DateTimeField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operator', null=True, blank=True)
    booking_status = models.CharField(max_length=20, default='pending', choices=BOOKING_STATUS)

    def __str__(self):
        return str(self.uuid)

