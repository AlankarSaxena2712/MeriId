from rest_framework import serializers

from general.models import *


class Guidelines(serializers.ModelSerializer):
    class Meta:
        model = Guidelines
        fields = "__all__"


class Feedback(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"