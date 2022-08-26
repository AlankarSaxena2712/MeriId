from datetime import datetime

from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request

from booking.models import Booking, Friend, Order, Payment
from booking.serializers import BookingSerializer
from services.response import create_response, success_response, bad_request_response
from services.twillio import send_twilio_message
from services.utility import create_hash, create_otp
from users.models import Address, Attendance

User = get_user_model()


@permission_classes((IsAuthenticated, ))
class BookingView(generics.RetrieveAPIView, generics.CreateAPIView):
    """
    booking serializer
    """
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        response = []
        bookings = Booking.objects.filter(user=request.user)
        for booking in bookings:
            friends = booking.friends.all()
            res = {
                "address": f"{booking.address.address_line_1}, {booking.address.address_line_2}, {booking.address.city}, {booking.address.state}, {booking.address.pincode}",
                "uuid": booking.uuid,
                "booking_id": booking.booking_id,
                "slot_date": booking.slot_date,
                "slot_time": booking.slot_time if booking.slot_time else "",
                "friends": [],
                "operator": {
                    "name": booking.operator.name if booking.operator else "",
                    "phone_number": booking.operator.phone_number if booking.operator else ""
                },
                "status": booking.booking_status,
                "preference": booking.preference,
            }
            for friend in friends:
                res["friends"].append({
                        "name":friend.name,
                        "phone_number":friend.phone_number,
                })
            response.append(res)
        return success_response(response)

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
                preference="male" if data['preference'] == None else "female",
                slot_time=data['slot_time'],
                address=address,
            )
            booking.save()
            friends = []
            for fr in data['friends']:
                if fr["name"] is not None:
                    friend = Friend(
                        name=fr['name'],
                        phone_number=fr['phone_number'],
                        reason=fr['reason'],
                        booking_type=fr['booking_type'],
                    )
                    friend.save()
                    friends.append(friend)
            booking.friends.set(friends)
            payment = Payment(
                amount=data["payment"]["amount"],
                from_user=data["payment"]["from_user"],
                booking=booking
            )
            payment.save()
            return create_response({'booking_id': booking.uuid})
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
            },
            "gender": "female"
        }
        bking = Booking.objects.get(uuid=booking)
        operator = bking.operator
        response['operator']['lat'] = operator.address.latitude
        response['operator']['lng'] = operator.address.longitude
        response['booking']['lat'] = bking.address.latitude
        response['booking']['lng'] = bking.address.longitude
        if bking.preference is None:
            response["gender"] = "male"
        else:
            response["gender"] = "female"
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
            booking = Booking.objects.get(booking_id=data['booking_id'])
            order = Order.objects.get(booking=booking)
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

    
@permission_classes((IsAuthenticated, ))
class AdminWiseBookingList(generics.RetrieveAPIView):
    """
    Retrieve booking
    """
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        try:
            admin = request.user
            pincodes = admin.pincodes.values_list('pincode', flat=True)
            bookings = Booking.objects.filter(address__pincode__in=pincodes, slot_date=datetime.now().date())
            response = []
            for bking in bookings:
                res = {}
                res['uuid'] = bking.uuid
                res['booking_id'] = bking.booking_id
                res['slot_date'] = bking.slot_date
                res['created_at'] = bking.created_at
                res['name'] = bking.user.name
                addre = bking.address.address_line_1 + ', ' + bking.address.address_line_2 + ', ' + bking.address.city + ', ' + bking.address.state
                res['address'] = addre
                res['pincode'] = bking.address.pincode
                res['slot_time'] = bking.slot_time
                res['operator'] = bking.operator.name if bking.operator else None
                res['preference'] = bking.preference
                res['status'] = bking.booking_status
                response.append(res)
            return success_response(response)
        except Exception as e:
            return bad_request_response(str(e))

    
@permission_classes((IsAuthenticated, ))
class AdminWiseBookingUpdateApi(generics.RetrieveUpdateAPIView):
    """
    Retrieve booking
    """
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        try:
            bookings = Booking.objects.get(booking_id=kwargs.get('booking_id'))
            response = []
            for bking in bookings:
                res = {}
                res['uuid'] = bking.uuid
                res['booking_id'] = bking.booking_id
                res['slot_date'] = bking.slot_date
                res['created_at'] = bking.created_at
                res['name'] = bking.user.name
                addre = bking.address.address_line_1 + ', ' + bking.address.address_line_2 + ', ' + bking.address.city + ', ' + bking.address.state
                res['address'] = addre
                res['pincode'] = bking.address.pincode
                response.append(res)
            return success_response(response)
        except Exception as e:
            return bad_request_response(str(e))

    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            operator = User.objects.get(uuid=data['operator'])
            time_slot = data["time_slot"]
            booking = Booking.objects.get(booking_id=data['booking_id'])
            booking.booking_status = "accepted"
            booking.operator = operator
            booking.slot_time = time_slot
            booking.save()
            attendance = Attendance.objects.get(user=operator, date=datetime.now().date())
            if time_slot == "10:00 AM - 11:00 AM":
                attendance.slot_10_to_11 = True
            elif time_slot == "11:00 AM - 12:00 PM":
                attendance.slot_11_to_12 = True
            elif time_slot == "12:00 PM - 1:00 PM":
                attendance.slot_12_to_1 = True
            elif time_slot == "1:00 PM - 2:00 PM":
                attendance.slot_1_to_2 = True
            elif time_slot == "2:00 PM - 3:00 PM":
                attendance.slot_2_to_3 = True
            elif time_slot == "3:00 PM - 4:00 PM":
                attendance.slot_3_to_4 = True
            elif time_slot == "4:00 PM - 5:00 PM":
                attendance.slot_4_to_5 = True
            elif time_slot == "5:00 PM - 6:00 PM":
                attendance.slot_5_to_6 = True
            attendance.save()
            return success_response({'message': 'Booking status updated'})
        except Exception as e:
            return bad_request_response(str(e))


@permission_classes((IsAuthenticated, ))
class BookingOperatorSlot(generics.RetrieveUpdateAPIView):
    def get(self, request, *args, **kwargs):
        try:
            operator = kwargs['uuid']
            date = request.GET.get("date")
            oper = User.objects.get(uuid=operator)
            bookings = Booking.objects.filter(operator=oper, slot_date=date)
            response = []
            for booking in bookings:
                response.append({
                    "id": booking.booking_id,
                    "slot": booking.slot_time,
                    "status": booking.booking_status
                })
            return success_response(response)
        except Exception as e:
            return bad_request_response(str(e))


@permission_classes((IsAuthenticated, ))
class OperatorWiseBooking(generics.RetrieveAPIView):
    """
    Retrieve booking
    """
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        try:
            operator = request.user
            bookings = Booking.objects.filter(operator=operator).order_by('-booking_id')
            attendance = Attendance.objects.get(user=operator, date=datetime.now().date())
            response = []
            for bking in bookings:
                if attendance.status == "present" and bking.booking_status != "completed":
                    res = {}
                    res['uuid'] = bking.uuid
                    res['booking_id'] = bking.booking_id
                    res['date'] = bking.slot_date
                    res['name'] = bking.user.name
                    res['number'] = bking.user.phone_number
                    addre = bking.address.address_line_1 + ', ' + bking.address.address_line_2 + ', ' + bking.address.city + ', ' + bking.address.state + ", " + bking.address.pincode
                    res['address'] = addre
                    res['lat'] = bking.address.latitude
                    res['long'] = bking.address.longitude
                    res['no_of_people'] = bking.friends.count()
                    res['pincode'] = bking.address.pincode
                    res['time_slot'] = bking.slot_time
                    res['status'] = bking.booking_status
                    response.append(res)
            return success_response(response)
        except Exception as e:
            return bad_request_response(str(e))


@permission_classes((IsAuthenticated, ))
class BookingStatusUpdateByOperatorAPI(generics.UpdateAPIView):
    """
    Retrieve booking
    """
    serializer_class = BookingSerializer

    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            booking = Booking.objects.get(uuid=data['uuid'])
            booking.booking_status = data['status']
            booking.save()
            return success_response({'message': 'Booking status updated'})
        except Exception as e:
            return bad_request_response(str(e))


@permission_classes((IsAuthenticated, ))
class CreateHashedWebLinkForOperator(generics.CreateAPIView):
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):
        try:
            image_url = request.data["image_url"]
            operator_uuid = request.data["uuid"]
            booking_uuid = request.data["booking"]
            booking = Booking.objects.get(uuid=booking_uuid)
            booking.verification_image = image_url
            booking.booking_status = "completed"
            booking.save()
            new_code = operator_uuid + "--__--__--__--__--__--__--" + booking_uuid
            url = f"https://meriid.herokuapp.com/operator/verify/{new_code}"
            return success_response({"url": url})
        except Exception as e:
            return bad_request_response({"error": e})


def automatic_slot_booking():
    status_to_exclude = ['completed', 'operator_out']
    bookings = Booking.objects.filter(slot_date=datetime.now().date(), operator=None).exclude(booking_status__in=status_to_exclude)
    operators = User.objects.filter(role="operator", attendance_set__status="present")
    for booking in bookings:
        for operator in operators:
            if booking.address.pincode == operator.address.pincode:
                if booking.slot_time == "9:00 AM - 12:00 PM":
                    operator = None

