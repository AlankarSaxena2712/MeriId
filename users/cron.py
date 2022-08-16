import imp
from general.models import Notice

def my_scheduled_job():
    Notice.objects.create(
        title="Test",
        description="Test",
    )