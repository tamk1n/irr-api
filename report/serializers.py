from rest_framework import serializers
from .models import *
from division.serializers import *
from users.serializers import *


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


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportObservation
        fields = ['id', 'report', 'content', 'type', 'status']
    

class ObservationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportObservation
        fields = ['id', 'report', 'content', 'reference_doc', 'category', 'factor', 'type', 'status', 'action', 'deadline', 'close_date']      


class ObservationReadSerializer(ObservationDetailSerializer):
    category = ObservationCategorySerializer()
    factor = ObservationFactorSerializer()
    type = ObservationTypeSerializer()
    status = ObservationStatusSerializer()



class InspectionReportDetailSerializer(serializers.ModelSerializer):
    observations = ObservationDetailSerializer(many=True, read_only=True)
    division = DivisionSerializer()
    field = DivisionFieldSerializer()
    issued_by = ReadUserSerializer()

    class Meta:
        model = InspectionReport
        fields = ['id', 'project', 'division', 'field', 'issue_date', 'issued_by', 'observations', 'responsible_person']


class InspectionReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = InspectionReport
        fields = ['id', 'project', 'division', 'field', 'issue_date', 'issued_by', 'responsible_person']
        read_only_fields = ['issued_by']

    
    def create(self, validated_data):
        validated_data = {'issued_by': self.context['request'].user, **validated_data}
        instance = InspectionReport.objects.create(**validated_data)
        return instance


class ObservationEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationEvidence
        fields = '__all__'