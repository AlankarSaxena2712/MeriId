from django.urls import path

from users.views import *

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('otp-send', SendOtp.as_view(), name='otp-send'),
    # path('register', RegisterAPIView.as_view(), name='register'),
    path('profile', UserPrfile.as_view(), name='profile'),
    path('operators', OperatorList.as_view(), name='operator-list'),
    # path('operator/<int:pk>/', OperatorList.as_view(), name='operator-list'),
    path('users', UserList.as_view(), name='user-list'),
    # path('user/<int:pk>/', UserList.as_view(), name='user-list'),
]
