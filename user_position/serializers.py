from rest_framework.serializers import ModelSerializer
from .models import *


class UserPositionSerializer(ModelSerializer):
    class Meta:
        model = UserPosition
        fields = ['id', 'name', 'description']
