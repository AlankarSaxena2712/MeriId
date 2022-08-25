from django.urls import path

from users.views import *

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('login/admin', AdminLoginView.as_view(), name='admin-login'),
    path('otp-send', SendOtp.as_view(), name='otp-send'),
    path('profile', UserPrfile.as_view(), name='profile'),
    path('profile/operator', UserOperatorProfile.as_view(), name='profile-operator'),
    path('profile/user', UserProfileApiView.as_view(), name='profile-user'),
    path('operators', OperatorList.as_view(), name='operator-list'),
    path('operators/<str:uuid>', OperatorUpdateView.as_view(), name='operator-update'),
    path('users', UserList.as_view(), name='user-list'),
    path('user/status/update', UpdateUserStatus.as_view(), name='user-status-update'),
    path('user/docs/update', UpdateUserDocumentLink.as_view(), name='user-docs-update'),
    path("operator-add", AddOperator.as_view(), name="operator-add"),
    path("issue", IssueView.as_view(), name="issue"),
    path("current-status", CurrentUserStatusApi.as_view(), name="current-status"),
    path("kyc/type", UserSetKycTypeApi.as_view(), name="kyc-type"),
    path("kyc/docs", KycView.as_view(), name="kyc-docs"),
    path("attendance", AttendanceView.as_view(), name="attendance"),
    path("attendance/download", DownloadAttendanceView.as_view(), name="attendance-download"),
    path("attendance/punch-out", AttendancePunchOutView.as_view(), name="attendance-punch-out"),
    path("admin/operator/list", AdminWiseOperatorListView.as_view(), name="admin-wise-operator-list"),
    path("operator/time_slot/<str:uuid>", OperatorWiseTimeSlotsApiView.as_view(), name="operator-time-slot"),
    path("send-noti", send_noti, name="send-noti"),
    path("operator/location/<str:uuid>", OperatorLocationView.as_view(), name="operator_location"),
    path("operator/location/update/<str:uuid>", LocationUpdateApiView.as_view(), name="location-update"),
    path("operator/slot/release/<str:uuid>", ReleaseOperatorSlot.as_view(), name="release-operator-slot"),
    path('sms', GetMessageFromTwilio.as_view(), name="get-message-from-twilio")
]
