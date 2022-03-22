from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from services.response import create_response, success_response, bad_request_response
from services.twillio import send_twilio_message
from services.utility import create_otp, create_token

from users.serializers import LoginSerializer, OtpSendSerializer, UserSerializer, AadharCardSerializer

User = get_user_model()


@permission_classes([AllowAny])
class SendOtp(generics.CreateAPIView):
    serializer_class = OtpSendSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = User.objects.filter(phone_number=phone_number).first()
            if user:
                otp = create_otp()
                user.set_password(otp)
                user.save()
                send_twilio_message(phone_number, otp)
                return success_response({'message': "success"})
            return bad_request_response({'message': 'User not found'})
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
            user.set_password(request.data["otp"])
            user.save()
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
            elif not user.is_active:
                return bad_request_response({"message": "Your phone number isn't verified! Please verify than try to login."})
            else:
                return bad_request_response({"message": "Invalid OTP!"})


# @permission_classes((AllowAny, ))
# class RegisterAPIView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid():
#             return bad_request_response(serializer.errors)
#         check_user = User.objects.filter(username=request.data["email"])
#         if not check_user:
#             user = User.objects.create_user(
#                 first_name=request.data['first_name'],
#                 last_name=request.data['last_name'],
#                 username=request.data['email'],
#                 email=request.data['email'],
#                 password=request.data['password'],
#                 is_active=True,
#                 phone_number=request.data['phone_number']
#             )
#             user.save()
#             return create_response({"message": "User Created Successfully"})
#         else:
#             return bad_request_response({"message": "User with this email already exsist."})

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
