from django.urls import path

from django.views.decorators.csrf import csrf_exempt

from general.views import FeedbackView, GuidelinesView, NoticeView, AadharAddressPrePopulateAPI, sendXml

urlpatterns = [
    path("guidelines", GuidelinesView.as_view(), name="guidelines"),
    path("feedback", FeedbackView.as_view(), name="feedback"),
    path("notice", NoticeView.as_view(), name="notice"),
    path("populate-address/<str:aadhar>", AadharAddressPrePopulateAPI.as_view(), name="populate-address"),
    path("get_xml", csrf_exempt(sendXml), name="sendXMl")
    # path("phone-number-otp", otpTelegram(), name="telegram"),
]
