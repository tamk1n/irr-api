from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import *
from .models import *


class UserPositionAPIView(ListAPIView):
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionSerializer


class UserPositionDetailView(RetrieveAPIView):
    serializer_class = UserPositionSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = UserPosition.objects.filter(id=self.kwargs['id'])
        return queryset




