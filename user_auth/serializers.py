from rest_framework import serializers
from users.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class AddEmployeeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    position = serializers.IntegerField()

    def validate(self, data):
        """Check if user with requested email already exists"""
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError('This employee is already registered.')
        
        return data