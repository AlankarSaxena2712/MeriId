import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from services.constants import USER_ROLE, USER_STATUS


class User(AbstractUser):
    """
    User model
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=255, choices=USER_STATUS)
    aadhar_limit = models.IntegerField(default=5)
    profile = models.URLField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=30, choices=USER_ROLE, default='user')

    def save(self, *args, **kwargs):
        if len(self.phone_number) == 10:
            self.username = self.phone_number
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.uuid)


class Kyc(models.Model):
    """
    KYC model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aadhar_card = models.URLField(max_length=255, blank=True, null=True)
    aadhar_card_data = models.CharField(max_length=255, blank=True, null=True)
    pan_card = models.URLField(max_length=255, blank=True, null=True)
    pan_card_data = models.CharField(max_length=255, blank=True, null=True)
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
    issue = models.TextField()

    def __str__(self):
        return str(self.uuid)
