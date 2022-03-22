import uuid as uuid
from django.db import models


class Guidelines(models.Model):
    """
    Guidelines model
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guideline = RichTextField()
    user_type = models.CharField(max_length=30, choices=USER_ROLE)

    def __str__(self):
        return self.uuid


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

