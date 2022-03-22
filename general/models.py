import uuid as uuid

from django.contrib.auth import get_user_model
from django.db import models

from ckeditor.fields import RichTextField

from services.constants import USER_ROLE, RATING_CHOICES

User = get_user_model()


class Guidelines(models.Model):
    """
    Guidelines model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guideline = RichTextField()
    user_type = models.CharField(max_length=30, choices=USER_ROLE)

    def __str__(self):
        return self.uuid

    class Meta:
        verbose_name_plural = "Guidelines"


class Feedback(models.Model):
    """
    FeedBack model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedback_for")
    rating = models.IntegerField(choices=RATING_CHOICES)
    feedback = models.TextField()

    def __str__(self):
        return self.uuid

