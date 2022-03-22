from django.urls import path

from general.views import FeedbackView, GuidelinesView

urlpatterns = [
    path("guidelines", GuidelinesView.as_view(), name="guidelines"),
    path("feedback", FeedbackView.as_view(), name="feedback"),
]
