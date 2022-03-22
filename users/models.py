import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from services.constants import USER_ROLE


class User(AbstractUser):
    """
    User model
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, unique=True)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=6)
    status = models.CharField(max_length=255)
    aadhar_limit = models.IntegerField(default=5)
    profile = models.URLField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=30, choices=USER_ROLE, default='user')
    other_documents = models.URLField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if len(self.phone_number) == 10:
            self.username = self.phone_number
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.uuid)


class AadharCard(models.Model):
    """
    Aadharcard model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_status = models.BooleanField(default=False)
    aadhar_number = models.CharField(max_length=12)
    phone_number_linked_to_aadhar = models.CharField(max_length=10)

    def __str__(self):
        return self.uuid
