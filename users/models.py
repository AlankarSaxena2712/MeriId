import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from services.constants import ATTENDANCE_STATUS, USER_ROLE, USER_STATUS


class Address(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.address_line_1


class User(AbstractUser):
    """
    User model
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=255, choices=USER_STATUS, default="kyc")
    kyc_status = models.BooleanField(default=False, help_text="False for (aadhar, pan and video) else True for (other and video)") # False for (aadhar, pan and video) else True for (other and video) 
    aadhar_limit = models.IntegerField(default=5)
    profile = models.URLField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=30, choices=USER_ROLE, default='user')
    address = models.OneToOneField(Address, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        if len(self.phone_number) == 10:
            self.username = self.phone_number
        if self.kyc_status:
            self.status = "other"
        else:
            self.status = "pan"
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + " - " + self.role


class Kyc(models.Model):
    """
    KYC model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhar_card = models.URLField(max_length=255, blank=True, null=True)
    pan_card = models.URLField(max_length=255, blank=True, null=True)
    other_documents = models.URLField(max_length=255, blank=True, null=True)
    video_link = models.URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Issue(models.Model):
    """
    Issue model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False ,  unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return str(self.uuid)


class Attendance(models.Model):
    """
    Attendace model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False ,  unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    punch_in = models.TimeField()
    punch_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=ATTENDANCE_STATUS, default='absent')
    slot_10_to_11 = models.BooleanField(default=False, help_text="False if operator is busy in this slot else True")
    slot_11_to_12 = models.BooleanField(default=False, help_text="False if operator is busy in this slot else True")
    slot_12_to_1 = models.BooleanField(default=False, help_text="False if operator is busy in this slot else True")
    slot_1_to_2 = models.BooleanField(default=False, help_text="False if operator is busy in this slot else True")
    slot_2_to_3 = models.BooleanField(default=False, help_text="False if operator is busy in this slot else True")
    slot_3_to_4 = models.BooleanField(default=False, help_text="False if operator is busy in this slot else True")
    slot_4_to_5 = models.BooleanField(default=False, help_text="False if operator is busy in this slot else True")
    slot_5_to_6 = models.BooleanField(default=False, help_text="False if operator is busy in this slot else True")

    def __str__(self):
        return str(self.user)
