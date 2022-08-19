import uuid as uuid
from django.contrib.auth import get_user_model
from django.db import models

from services.constants import BOOKING_SLOT_TIME, BOOKING_STATUS, BOOKING_TYPE
from users.models import Address

User = get_user_model()


class Friend(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Create your models here.
class Booking(models.Model):
    """
    bookin model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(Friend)
    slot_date = models.DateField(null=True)
    slot_time = models.CharField(max_length=20, blank=True, null=True, choices=BOOKING_SLOT_TIME) 
    operator_arrival_time = models.DateTimeField(null=True, blank=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operator', null=True, blank=True)
    verification_image = models.URLField(max_length=255, blank=True, null=True)
    booking_status = models.CharField(max_length=20, default='pending', choices=BOOKING_STATUS)
    booking_type = models.CharField(max_length=20, blank=True, null=True, choices=BOOKING_TYPE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uuid)


class Order(models.Model):
    """
    bookin model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, blank=True, null=True)
    booking = models.OneToOneField(Address, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)