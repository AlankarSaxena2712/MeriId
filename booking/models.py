import uuid as uuid
from django.contrib.auth import get_user_model


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
    operator_arrival_time = models.DateTimeField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operator', null=True, blank=True)


    def __str__(self):
        return str(self.uuid)

