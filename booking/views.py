from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from booking.models import Booking
from booking.serializers import BookingSerializer
from services.response import success_response, bad_request_response

User = get_user_model()


@permission_classes((IsAuthenticated, ))
class BookingView(generics.RetrieveAPIView, generics.CreateAPIView):
    """
    booking serializer
    """
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(Booking.objects.all(), many=True)
        return success_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated, ))
class OperatorBookingLocationView(generics.RetrieveAPIView):
    """
    Retrieve booking location
    """
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        booking = kwargs.get('booking_uuid')
        response = {
            "operator": {
                "lat": "",
                "lng": ""
            },
            "booking": {
                "lat": "",
                "lng": "",
            }
        }
        bking = Booking.objects.get(uuid=booking)
        operator = bking.operator
        response['operator']['lat'] = operator.address.latitude
        response['operator']['lng'] = operator.address.longitude
        response['booking']['lat'] = bking.address.latitude
        response['booking']['lng'] = bking.address.longitude
        return success_response(response)


