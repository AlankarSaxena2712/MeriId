import uuid
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from booking.models import Booking, Friend
from booking.serializers import BookingSerializer
from services.response import create_response, success_response, bad_request_response
from users.models import Address

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
        try:
            data = request.data
            address = Address(
                address_line_1=data['address']['address_line_1'],
                address_line_2=data['address']['address_line_2'],
                city=data['address']['city'],
                state=data['address']['state'],
                pincode=data['address']['pincode'],
                latitude=data['address']['latitude'],
                longitude=data['address']['longitude']
            )
            address.save()
            booking = Booking(
                user=request.user,
                slot_date=data['slot_date'],
                booking_type=data['booking_type'],
                address=address,
            )
            booking.save()
            friends = []
            for fr in data['friends']:
                friend = Friend(
                    name=fr['name'],
                    phone_number=fr['phone_number'],
                    reason=fr['reason'],
                )
                friend.save()
                friends.append(friend)
            booking.friends.set(friends)
            return create_response({'message': 'Booking created successfully'})
        except Exception as e:
            return bad_request_response(str(e))


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


