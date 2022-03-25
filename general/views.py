from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from general.models import Feedback, Guidelines
from general.serializers import FeedbackSerializer, GuidelinesSerializer
from services.response import success_response, bad_request_response


@permission_classes((AllowAny, ))
class GuidelinesView(generics.RetrieveAPIView):
    """
    Retrieve guidelines
    """
    serializer_class = GuidelinesSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(Guidelines.objects.all(), many=True)
        return success_response(serializer.data)


@permission_classes((IsAuthenticated, ))
class FeedbackView(generics.RetrieveAPIView, generics.CreateAPIView):
    """
    Retrieve feedback
    """
    serializer_class = FeedbackSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(Feedback.objects.all(), many=True)
        return success_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)
