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
    time = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User , related_name='friends')

    def __str__(self):
        return str(self.uuid)

