from rest_framework import serializers
from rest_framework.exceptions import NotFound
from .models import *
from users.serializers import *


class CompanySerializer(serializers.ModelSerializer):
    employees = UserProfileSerializer(many=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'employees']


class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description']


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'name', 'company', 'description']
        extra_kwargs = {'company': {'write_only': True}}

    def validate(self,  data):
        company = data.get('company')
        if self.context['request'].user.my_profile.company != company:
            raise serializers.ValidationError('Company not found')
        
        return data


class DivisionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DivisionField
        fields = ['id', 'name', 'division', 'description']
        extra_kwargs = {'division': {'write_only': True}}

    def validate(self,  data):
        division = data.get('division')
        if division not in self.context['request'].user.my_profile.company.divisions.all():
            raise NotFound('Division not found')
        return data