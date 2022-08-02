from rest_framework import serializers

from users.models import *


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)
    otp = serializers.CharField(max_length=6)

    class Meta:
        fields = ['phone_number', 'otp']

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=75)
    password = serializers.CharField(required=True, max_length=50)

    class Meta:
        fields = ['email', 'password']

    @classmethod
    def validate_email(cls, value):
        return value.lower()


class OtpSendSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=10)

    class Meta:
        fields = ['phone_number']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class KycSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kyc
        fields = "__all__"


class OperatorAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "uuid",
            "phone_number",
            "name",
            "email",
            "role",
            "state",
            "city",
            "pin_code",
        ]
        read_only_fields = [
            "id",
            "uuid",
        ]



class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "status",
        ]
