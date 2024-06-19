from rest_framework import serializers
from users.models import UserProfile
from django.contrib.auth import get_user_model
from .models import *

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
    

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['otp', 'email', 'is_active']
        read_only_fields = ('expire_date', )
    
    def validate(self, data):
        if data.get('email') and not User.objects.filter(email=data['email'], is_active=True).exists():
            raise serializers.ValidationError('The user with this email does not exist.')
        return data
    
