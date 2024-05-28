from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from .serializers import WriteUserSerializer

User = get_user_model()


class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = WriteUserSerializer




