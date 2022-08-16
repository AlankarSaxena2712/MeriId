import uuid as uuid

from django.contrib.auth import get_user_model
from django.db import models

from ckeditor.fields import RichTextField
from booking.models import Booking

from services.constants import USER_ROLE, RATING_CHOICES

User = get_user_model()


class Guidelines(models.Model):
    """
    Guidelines model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guideline = RichTextField()
    user_type = models.CharField(max_length=30, choices=USER_ROLE, unique=True)

    def __str__(self):
        return self.user_type

    class Meta:
        verbose_name_plural = "Guidelines"


class Feedback(models.Model):
    """
    FeedBack model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="operator_feedback", null=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    description = models.TextField()

    def __str__(self):
        return str(self.uuid)


class Notice(models.Model):
    """
    Notice model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='notice/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)

    class Meta:
        verbose_name_plural = "Notices"
