from rest_framework import serializers
from django.contrib.auth import get_user_model
from user_position.serializers import UserPositionSerializer
from .models import UserProfile

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'position']


class ReadUserSerializer(BaseUserSerializer):
    position = UserPositionSerializer()

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + ['position']


class WriteUserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + ['position', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = ReadUserSerializer()
    class Meta:
        model = UserProfile
        fields = ['user']
