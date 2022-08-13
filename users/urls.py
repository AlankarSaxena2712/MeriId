from django.urls import path

from users.views import *

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('login/admin', AdminLoginView.as_view(), name='admin-login'),
    path('otp-send', SendOtp.as_view(), name='otp-send'),
    path('profile', UserPrfile.as_view(), name='profile'),
    path('operators', OperatorList.as_view(), name='operator-list'),
    path('operators/<str:uuid>', OperatorUpdateView.as_view(), name='operator-update'),
    path('users', UserList.as_view(), name='user-list'),
    path("operator-add", AddOperator.as_view(), name="operator-add"),
    path("issue", IssueView.as_view(), name="issue"),
    path("current-status", CurrentUserStatusApi.as_view(), name="current-status"),
    path("kyc/type", UserSetKycTypeApi.as_view(), name="kyc-type"),
    path("kyc/docs", KycView.as_view(), name="kyc-docs"),
]
