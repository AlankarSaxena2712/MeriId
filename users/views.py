import csv
from datetime import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, HttpResponse

from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from services.response import create_response, success_response, bad_request_response
from services.twillio import send_twilio_message
from services.utility import create_otp, create_token
from users.models import Address, Attendance, Issue, Kyc

from users.serializers import AdminLoginSerializer, AttendanceSerializer, LoginSerializer, OperatorAddSerializer, \
    OtpSendSerializer, UserSerializer, KycSerializer, IssueSerializer, UserSetKycTypeSerializer, UserStatusSerializer

User = get_user_model()


@permission_classes([AllowAny])
class SendOtp(generics.CreateAPIView):
    serializer_class = OtpSendSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            role = serializer.validated_data['role']
            user = User.objects.filter(phone_number=phone_number).first()
            otp = create_otp()
            if role == "operator":
                if user:
                    user.set_password(otp)
                    user.save()
                    send_twilio_message(phone_number, otp)
                    return success_response({'message': "success"})
            elif role == "user":
                if user:
                    user.set_password(otp)
                    user.save()
                    send_twilio_message(phone_number, otp)
                else:
                    new_user = User.objects.create_user(username=phone_number, phone_number=phone_number, password=otp)
                    new_user.save()
                    send_twilio_message(phone_number, otp)
                return success_response({'message': "success"})
        return bad_request_response(serializer.errors)


@permission_classes((AllowAny,))
class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serialzer = self.get_serializer(data=request.data)
        if not serialzer.is_valid():
            return bad_request_response(serialzer.errors)
        if request.data["phone_number"] is not None or request.data['phone_number'] != "":
            user = generics.get_object_or_404(User, phone_number=request.data["phone_number"])
            if user:
                if user.check_password(request.data["otp"]):
                    token = create_token(username=user.username, password=request.data["otp"])
                    if token:
                        response = {
                            "token": token.key,
                            "user": {
                                "first_name": user.name,
                                "email": user.email,
                                "phone_number": user.phone_number,
                            }
                        }
                        if user.role == "user":
                            user.status = "kyc"
                            user.save()
                        return create_response(response)
        return bad_request_response({"message": "Invalid OTP!"})


@permission_classes((AllowAny,))
class AdminLoginView(generics.CreateAPIView):
    serializer_class = AdminLoginSerializer

    def post(self, request, *args, **kwargs):
        serialzer = self.get_serializer(data=request.data)
        if not serialzer.is_valid():
            return bad_request_response(serialzer.errors)
        if request.data["email"] is not None or request.data['email'] != "":
            user = get_object_or_404(User, email=request.data["email"])
            token = create_token(username=user.username, password=request.data['password'])
            if token:
                return create_response({'token': token.key})
            else:
                return bad_request_response({"message": "Invalid Username/Password"})


@permission_classes((IsAuthenticated, ))
class UpdateUserStatus(generics.CreateAPIView):
    serializer_class = UserStatusSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.get(uuid=request.user.uuid)
        user.status = data["status"]
        if data["status"] == "pan":
            user.kyc_status = False
        elif data["status"] == "other":
            user.kyc_status = True
        else:
            return bad_request_response({"message": "wrong status"})
        user.save()
        return success_response({"status": user.status})


@permission_classes((IsAuthenticated,))
class UserPrfile(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return success_response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated,))
class UserOperatorProfile(generics.RetrieveAPIView):
    serializer_class = OperatorAddSerializer

    def get(self, request, *args, **kwargs):
        attendance = Attendance.objects.get(user=request.user, date=datetime.now().date()).status
        response = {
            "uuid": request.user.uuid,
            "name": request.user.name,
            "email": request.user.email,
            "number": request.user.phone_number,
            "userId": request.user.user_id,
            "status": request.user.status,
            "attendance": attendance
        }
        return success_response(response)


@permission_classes((IsAuthenticated,))
class OperatorList(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(role='operator')
        response = []
        for user in users:
            response.append({
                "id": user.uuid,
                "name": user.name,
                "email": user.email,
                "phone_number": user.phone_number,
                "city": user.address.city,
                "state": user.address.state,
                "pin_code": user.address.pincode,
            })
        return success_response(response)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated,))
class OperatorUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OperatorAddSerializer

    def get_object(self):
        return get_object_or_404(User, uuid=self.kwargs['uuid'])

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return success_response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return success_response({"message": "User deleted successfully"})


@permission_classes((IsAuthenticated,))
class UserList(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(role='user')
        serializer = self.get_serializer(users, many=True)
        return success_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated,))
class AddOperator(generics.CreateAPIView):
    serializer_class = OperatorAddSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            address = Address(
                state=data["state"],
                city=data["city"],
                pincode=data["pin_code"]
            )
            address.save()
            new_user = User.objects.create_user(
                username=data["phone_number"],
                phone_number=data["phone_number"],
                name=data["name"],
                email=data["email"],
                password="1234",
                role="operator",
                address=address
            )
            new_user.save()
            return success_response({"message": "Operator added successfully"})
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated,))
class IssueView(generics.RetrieveAPIView):
    serializer_class = IssueSerializer

    def get(self, request, *args, **kwargs):
        users = Issue.objects.all()
        serializer = self.get_serializer(users, many=True)
        return success_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated,))
class CurrentUserStatusApi(generics.RetrieveAPIView):
    serializer_class = UserStatusSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return success_response(serializer.data)


@permission_classes((IsAuthenticated,))
class UserSetKycTypeApi(generics.CreateAPIView):
    serializer_class = UserSetKycTypeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated,))
class KycView(generics.CreateAPIView):
    serializer_class = KycSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        kyc = Kyc.objects.filter(user=request.user)
        user = User.objects.get(id=request.user.id)
        if len(kyc) > 0:
            if user.kyc_status == False:
                if data["aadhar_card"] is not None:
                    kyc.update(aadhar_card=data["aadhar_card"])
                    user.status = "video"
                    user.save()
                elif data["video_link"] is not None:
                    kyc.update(video_link=data["video_link"])
                    user.status = "pending"
                    user.save()
            else:
                if data["video_link"] is not None:
                    kyc.update(video_link=data["video_link"])
                    user.status = "pending"
                    user.save()
        else:
            if user.kyc_status == False:
                if data["pan_card"] is not None:
                    new_kyc = Kyc(
                        user=user,
                        aadhar_card=None,
                        pan_card=data["pan_card"],
                        other_documents=None,
                        video_link=None
                    )
                    user.kyc_status = False
                    user.status = "aadhar"
                    user.save()
            else:
                if data["other_documents"] is not None:
                    new_kyc = Kyc(
                        user=user,
                        aadhar_card=None,
                        pan_card=None,
                        other_documents=data["other_documents"],
                        video_link=None
                    )
                    user.kyc_status = True
                    user.status = "video"
                    user.save()
            new_kyc.save()
        return success_response({"message": "Kyc added successfully"})


@permission_classes((IsAuthenticated,))
class AttendanceView(generics.CreateAPIView):
    serializer_class = AttendanceSerializer

    def get(self, request, *args, **kwargs):
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        operator = request.GET.get("operator")
        op = User.objects.get(uuid=operator)
        attendance = Attendance.objects.filter(user=op, date__range=[date_from, date_to])
        serializer = self.get_serializer(attendance, many=True)
        return success_response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        date = data["date"]
        punch_in = data["punch_in"]
        try:
            attendance = Attendance.objects.get(user=request.user, date=date)
            attendance.punch_in = punch_in
            attendance.status = "present"
            attendance.save()
        except Attendance.DoesNotExist:
            attendance = Attendance(
                user=request.user,
                date=date,
                punch_in=punch_in,
                status="present"
            )
            attendance.save()
        return success_response({"message": "Attendance added successfully"})


@permission_classes((IsAuthenticated,))
class AttendancePunchOutView(generics.CreateAPIView):
    serializer_class = AttendanceSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        date = data["date"]
        punch_out = data["punch_out"]
        try:
            attendance = Attendance.objects.get(user=request.user, date=date)
            attendance.punch_out = punch_out
            attendance.status = "done"
            attendance.save()
        except Attendance.DoesNotExist:
            return bad_request_response({"message": "Attendance not found"})
        return success_response({"message": "Attendance added successfully"})


@permission_classes((IsAuthenticated,))
class DownloadAttendanceView(generics.RetrieveAPIView):
    serializer_class = AttendanceSerializer

    def get(self, request, *args, **kwargs):
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        operator_uuid = request.GET.get("operator")
        try:
            operator = User.objects.get(uuid=operator_uuid)
            attendance = Attendance.objects.filter(user=operator, date__range=[date_from, date_to])
            response = HttpResponse(content_type='text/csv')
            response[
                'Content-Disposition'] = f'attachment; filename="attendance-{operator.name}-{date_from}-{date_to}.csv"'
            writer = csv.writer(response)
            writer.writerow(['User', 'Date', 'Punch In', 'Punch Out', 'Status'])
            for a in attendance:
                writer.writerow([a.user.name, a.date, a.punch_in, a.punch_out, a.status])
            return response
        except User.DoesNotExist:
            return bad_request_response({"message": "Operator not found"})
        except Exception as e:
            return bad_request_response({"message": str(e)})


def send_noti(request):
    from firebase_admin.messaging import Message, Notification
    Message(
        notification=Notification(title="title", body="text", image="url"),
        topic="Optional topic parameter: Whatever you want",
    )
    return HttpResponse("ok")


@permission_classes((IsAuthenticated,))
class AdminWiseOperatorListView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        admin = request.user
        pincodes = admin.pincodes.values_list("pincode", flat=True)
        operators = User.objects.filter(address__pincode__in=pincodes, role="operator")
        response = []
        for operator in operators:
            response.append({
                "id": operator.id,
                "name": operator.name,
                "uuid": operator.uuid,
                "operator_id": operator.user_id,
            })
        return success_response(response)


@permission_classes((IsAuthenticated,))
class OperatorWiseTimeSlotsApiView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        operator = User.objects.get(uuid=kwargs["uuid"])
        date = request.GET.get("date")
        attendance = Attendance.objects.get(user=operator, date=date)
        time_slots = []
        time_slots.append({
            "slot": "10:00 AM - 11:00 AM",
            "status": attendance.slot_10_to_11
        })
        time_slots.append({
            "slot": "11:00 AM - 12:00 PM",
            "status": attendance.slot_11_to_12
        })
        time_slots.append({
            "slot": "12:00 PM - 1:00 PM",
            "status": attendance.slot_12_to_1
        })
        time_slots.append({
            "slot": "1:00 PM - 2:00 PM",
            "status": attendance.slot_1_to_2
        })
        time_slots.append({
            "slot": "2:00 PM - 3:00 PM",
            "status": attendance.slot_2_to_3
        })
        time_slots.append({
            "slot": "3:00 PM - 4:00 PM",
            "status": attendance.slot_3_to_4
        })
        time_slots.append({
            "slot": "4:00 PM - 5:00 PM",
            "status": attendance.slot_4_to_5
        })
        time_slots.append({
            "slot": "5:00 PM - 6:00 PM",
            "status": attendance.slot_5_to_6
        })
        return success_response(time_slots)


@permission_classes((IsAuthenticated,))
class OperatorLocationView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        operator = User.objects.get(uuid=kwargs["uuid"], role="operator")
        status = Attendance.objects.get(user=operator, date=datetime.now().date()).status
        response = {
            "lat": operator.address.latitude if operator.address else None,
            "long": operator.address.longitude if operator.address else None,
            "status": status
        }
        return success_response(response)


@permission_classes((IsAuthenticated,))
class LocationUpdateApiView(generics.UpdateAPIView):
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        address = Address.objects.get(user=request.user)
        address.latitude = request.data["lat"]
        address.longitude = request.data["long"]
        address.save()
        return success_response({"message": "Location updated successfully"})


@permission_classes((IsAuthenticated,))
class ReleaseOperatorSlot(generics.UpdateAPIView):
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        operator = User.objects.get(uuid=kwargs["uuid"])
        time_slot = request.data["slot"]
        attendance = Attendance.objects.get(user=operator, date=datetime.now().date())
        if time_slot == "10:00 AM - 11:00 AM":
            attendance.slot_10_to_11 = False
        elif time_slot == "11:00 AM - 12:00 PM":
            attendance.slot_11_to_12 = False
        elif time_slot == "12:00 PM - 1:00 PM":
            attendance.slot_12_to_1 = False
        elif time_slot == "1:00 PM - 2:00 PM":
            attendance.slot_1_to_2 = False
        elif time_slot == "2:00 PM - 3:00 PM":
            attendance.slot_2_to_3 = False
        elif time_slot == "3:00 PM - 4:00 PM":
            attendance.slot_3_to_4 = False
        elif time_slot == "4:00 PM - 5:00 PM":
            attendance.slot_4_to_5 = False
        elif time_slot == "5:00 PM - 6:00 PM":
            attendance.slot_5_to_6 = False
        attendance.save()
        return success_response({"message": "Slot released successfully"})
