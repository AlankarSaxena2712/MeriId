from rest_framework import serializers

from users.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AadharCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AadharCard
        fields = "__all__"
