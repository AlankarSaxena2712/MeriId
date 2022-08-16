from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from services.response import create_response, success_response, bad_request_response
from services.twillio import send_twilio_message
from services.utility import create_otp, create_token
from users.models import Attendance, Issue, Kyc

from users.serializers import AdminLoginSerializer, AttendanceSerializer, LoginSerializer, OperatorAddSerializer, OtpSendSerializer, UserSerializer, KycSerializer, IssueSerializer, UserSetKycTypeSerializer, UserStatusSerializer

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
            if role == "operator":
                if user:
                    otp = create_otp()
                    user.set_password(otp)
                    user.save()
            elif role == "user":
                if user:
                    otp = create_otp()
                    user.set_password(otp)
                    user.save()
                else:
                    otp = create_otp()
                    new_user = User.objects.create_user(username=phone_number, phone_number=phone_number, password=otp)
                    new_user.save()
            send_twilio_message(phone_number, otp)
            return success_response({'message': "success"})
        return bad_request_response(serializer.errors)


@permission_classes((AllowAny, ))
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
                        return create_response(response)
        return bad_request_response({"message": "Invalid OTP!"})


@permission_classes((AllowAny, ))
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


@permission_classes((IsAuthenticated, ))
class OperatorList(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(role='operator')
        serializer = self.get_serializer(users, many=True)
        return success_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated, ))
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


@permission_classes((IsAuthenticated, ))
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


@permission_classes((IsAuthenticated, ))
class AddOperator(generics.CreateAPIView):
    serializer_class = OperatorAddSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            new_user = User.objects.create_user(
                username=data["phone_number"],
                phone_number=data["phone_number"],
                name=data["name"],
                email=data["email"],
                password="1234",
                role="operator",
                state=data["state"],
                city=data["city"],
                pin_code=data["pin_code"],
            )
            new_user.save()
            return success_response({"message": "Operator added successfully"})
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated, ))
class IssueView(generics.RetrieveAPIView):
    serializer_class = IssueSerializer

    def get(self, request, *args, **kwargs):
        users = Issue.objects.all()
        serializer = self.get_serializer(users, many=True)
        return success_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated, ))
class CurrentUserStatusApi(generics.RetrieveAPIView):
    serializer_class = UserStatusSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return success_response(serializer.data)


@permission_classes((IsAuthenticated, ))
class UserSetKycTypeApi(generics.CreateAPIView):
    serializer_class = UserSetKycTypeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)


@permission_classes((IsAuthenticated, ))
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


@permission_classes((IsAuthenticated, ))
class AttendanceView(generics.CreateAPIView):
    serializer_class = AttendanceSerializer

    def get(self, request, *args, **kwargs):
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        attendance = Attendance.objects.filter(user=request.user, date__range=[date_from, date_to])
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
