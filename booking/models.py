from pyexpat import model
import uuid as uuid
from django.contrib.auth import get_user_model
from django.db import models

from services.constants import BOOKING_SLOT_TIME, BOOKING_STATUS, BOOKING_TYPE
from services.utility import UIDAI_address, create_booking_id
from users.models import Address

User = get_user_model()


class Friend(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    bookin model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField("booking.Booking", on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True, related_name='order_address')
    otp = models.CharField(max_length=6, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking.booking_id}"



class Booking(models.Model):
    """
    bookin model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_id = models.CharField(max_length=255, default=create_booking_id)
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

    def save(self, *args, **kwargs):
        super(Booking, self).save(*args, **kwargs)
        if self.booking_status == "completed":
            try:
                address = UIDAI_address()
                booking = Booking.objects.get(uuid=self.uuid)
                order = Order(
                    booking=booking,
                    address=address
                )
                order.save()
                super(Booking, self).save(*args, **kwargs)
            except Exception as e:
                pass

    def __str__(self):
        return f"{self.uuid}"