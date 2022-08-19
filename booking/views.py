import uuid
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from booking.models import Booking, Friend, Order
from booking.serializers import BookingSerializer
from services.response import create_response, success_response, bad_request_response
from services.twillio import send_twilio_message
from services.utility import create_otp
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


@permission_classes((AllowAny, ))
class OrderOtpSendAPI(generics.CreateAPIView):
    """
    Retrieve order
    """
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            booking = Booking.objects.get(booking_id=data['booking_id'])
            order = Order.objects.get(booking=booking)
            otp = create_otp()
            phone = order.booking.user.phone_number
            order.otp = otp
            order.save()
            send_twilio_message(phone, otp)
            return create_response({'message': 'Otp send'})
        except Exception as e:
            return bad_request_response(str(e))


@permission_classes((AllowAny, ))
class OrderOtpVerifyAPI(generics.CreateAPIView):
    """
    Retrieve order
    """
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            order = Order.objects.get(booking_id=data['booking_id'])
            if order.otp == data['otp']:
                response = {
                    "order_address": {
                        "address_line_1": order.address.address_line_1,
                        "address_line_2": order.address.address_line_2,
                        "city": order.address.city,
                        "state": order.address.state,
                        "pincode": order.address.pincode
                    },
                    "booking_address": {
                        "address_line_1": order.booking.address.address_line_1,
                        "address_line_2": order.booking.address.address_line_2,
                        "city": order.booking.address.city,
                        "state": order.booking.address.state,
                        "pincode": order.booking.address.pincode
                    },
                }
                return success_response(response)
            else:
                return bad_request_response('Otp not verified')
        except Exception as e:
            return bad_request_response(str(e))


