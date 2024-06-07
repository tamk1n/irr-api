from django.contrib.auth import get_user_model

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
from .serializers import AddEmployeeSerializer
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

