from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt import serializers

from users.serializers import ReadUserSerializer, WriteUserSerializer

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
