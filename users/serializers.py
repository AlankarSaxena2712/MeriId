from rest_framework import serializers

from users.models import *


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)
    otp = serializers.CharField(max_length=6)

    class Meta:
        fields = ['phone_number', 'otp']


class OtpSendSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=10)

    class Meta:
        fields = ['phone_number']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AadharCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AadharCard
        fields = "__all__"
