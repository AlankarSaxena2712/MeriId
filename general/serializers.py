from rest_framework import serializers

from general.models import *


class GuidelinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guidelines
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"