
import random
from datetime import datetime, timedelta
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
import time

from users.models import Address, Attendance

User = auth.get_user_model()


def create_token(username, password):
    user = auth.authenticate(username=username, password=password)
    if user and user.is_active:
        token, _ = Token.objects.get_or_create(user=user)
        return token
    return None

def create_otp():
    return ''.join(random.choice('0123456789') for i in range(6))

def create_booking_id():
    return "BOOK" + str(round(time.time() * 1000))

def UIDAI_address():
    try:
        address = Address.objects.get(address_line_1='UIDAI Office')
        return address
    except Exception as e:
        address = Address(
            address_line_1="UIDAI Office",
            address_line_2="Ground, Pragati Maidan",
            city="New Delhi",
            state="Delhi",
            pincode="110001",
            latitude="Latitude",
            longitude="Longitude"
        )
        address.save()
        return address

def create_attendance_for_next_day():
    operators = User.objects.filter(role='operator')
    for operator in operators:
        if Attendance.objects.filter(user=operator, date=datetime.now().date() + timedelta(days=1)).exists():
            pass
        else:
            attendance = Attendance(
                user=operator,
                date=datetime.now().date() + timedelta(days=1),
                status='absent'
            )
            attendance.save()


def create_hash(uuid):
    return make_password(uuid)

def check_hash(uuid, hash):
    return check_password(uuid, hash)
