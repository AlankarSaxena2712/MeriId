
import random
from django.contrib import auth
from rest_framework.authtoken.models import Token


def create_token(username, password):
    user = auth.authenticate(username=username, password=password)
    if user and user.is_active:
        token, _ = Token.objects.get_or_create(user=user)
        return token
    return None

def create_otp():
    return ''.join(random.choice('0123456789') for i in range(6))