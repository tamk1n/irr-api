import random
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt import serializers

from users.serializers import ReadUserSerializer, WriteUserSerializer
from .serializers import AddEmployeeSerializer, OTPSerializer
from .utils import AddEmployee
from .models import *
from division.permissions import IsUserManager


User = get_user_model()


class UserLoginView(TokenObtainPairView):
    serializer_class = serializers.TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        serialized_data = serializer.validated_data
        email = serializer.user.email
        user = User.objects.get(email=email)
        user_serializer = ReadUserSerializer(user)
        serialized_data = {**serialized_data, "userData": user_serializer.data}

        return Response(serialized_data, status=status.HTTP_200_OK)


class UserRegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = WriteUserSerializer


class AddEmployeeView(APIView):
    permission_classes = (IsAuthenticated, IsUserManager)

    def post(self, request, *args, **kwargs):
        serializer = AddEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            position_id = serializer.data.get('position')
            # generate and send register url
            token_url = AddEmployee(email, position_id).generate_token_url()
            response = {'url': token_url}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegisterEmployee(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, token):
        return AddEmployee().check_token(token)
    
    def get(self, request, token):
        token = self.get_object(token)
        response = {
            'email': token.email,
            'position': token.position.id
        }
        return Response(response, status=status.HTTP_200_OK)


class SendOTPAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        request.data['otp'] = str(random.randint(100000, 999999))
        serializer = OTPSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvalidateOTPView(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, request, otp):
        try:
            otp = OTP.objects.get(otp=otp, is_active=False)
            return otp
        except OTP.DoesNotExist:
            raise NotFound('OTP %s not valid' % otp)

    def patch(self, request, otp):
        otp = self.get_object(request, otp)
        request.data['otp'] = otp.otp
        request.data['email'] = otp.email
        request.data['is_active'] = True
        # request.data = {'otp': otp, 'email': otp.email, 'is_active': True, **request.data}
        serializer = OTPSerializer(otp, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ResetPasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        current_password = request.data['currentPassword']
        new_password = request.data['newPassword']
        if OTP.objects.filter(email=request.user.email, otp=request.data['otp'], is_active=False).first():
            return Response('OTP is incorrect', status=status.HTTP_400_BAD_REQUEST)

        if request.user.check_password(current_password):
            try:
                validate_password(new_password)
            except ValidationError as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(new_password)
            request.user.save()
            return Response('Password changed successfully', status=status.HTTP_200_OK)
        return Response('Password is incorrect', status=status.HTTP_400_BAD_REQUEST)
    
