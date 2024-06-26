from rest_framework import serializers
from .models import *


class ObservationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationType
        fields = '__all__'


class ObservationFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationFactor
        fields = '__all__'


class ObservationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationCategory
        fields = '__all__'


class ObservationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationStatus
        fields = '__all__'


class StaticDataSerializer(serializers.Serializer):
    type = ObservationTypeSerializer()
    factor = ObservationFactorSerializer()
    category = ObservationCategorySerializer()
    status = ObservationStatus()


class ReportAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionReport
        fields = '__all__'
