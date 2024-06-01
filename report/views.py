from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status

from .models import *
from .serializers import *
from .permissions import *
from .filters import *
from division.models import *
from users.models import *

class ObservationStaticDataAPIView(APIView):
    def get(self, request):
        response = dict()

        observations = ObservationType.objects.all()
        factors = ObservationFactor.objects.all()
        categories = ObservationCategory.objects.all()
        statuses = ObservationStatus.objects.all()

        response['type'] = ObservationTypeSerializer(observations, many=True).data
        response['factors'] = ObservationFactorSerializer(factors, many=True).data
        response['category'] = ObservationCategorySerializer(categories, many=True).data
        response['stasus'] = ObservationStatusSerializer(statuses, many=True).data

        return Response(response, status=status.HTTP_200_OK)


class ReportAPIView(GenericAPIView):
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = ReportFilter
    search_fields = ['project']
    ordering_fields = ['id', 'division__name']

    def get(self, request):
        try:
            company = request.user.my_profile.company
        except UserProfile.DoesNotExist():
            raise NotFound('Company not found!')
        
        divisions = company.divisions.all()
        queryset = InspectionReport.objects.filter(is_active=True, division__in=divisions)
        filtered_queryset = self.filter_queryset(queryset=queryset)
        queryset = self.paginate_queryset(filtered_queryset)
        serializer = InspectionReportSerializer(queryset, many=True)

        return self.get_paginated_response(serializer.data)


    def post(self, request):
        serializer = InspectionReportSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportDetailView(APIView):
    permission_classes = (IsAuthenticated, IsReportOwner)
    def get_object(self, report_id):
        try:
            report = InspectionReport.objects.get(id=report_id)
            self.check_object_permissions(self.request, report)
            return report
        except InspectionReport.DoesNotExist:
            raise NotFound(f'Inspection report for ID {report_id} not found')

    def get(self, request, report_id):
        report = self.get_object(report_id)
        serializer = InspectionReportDetailSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, report_id):
        report = self.get_object(report_id)
        serializer = InspectionReportSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, report_id):
        report = self.get_object(report_id)
        report.delete()
        return Response(f'Division field object deleted for given id: {report_id}', status=status.HTTP_204_NO_CONTENT)
    

class ObservationAPIView(GenericAPIView):
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = ObservationFilter
    search_fields = ['content']
    ordering_fields = ['id', 'division__name']    
    permission_classes = (IsAuthenticated, IsObsOwner)

    def get_object(self, report_id):
        try:
            report = InspectionReport.objects.get(id=report_id)
            self.check_object_permissions(self.request, report)
            return report
        except InspectionReport.DoesNotExist:
            raise NotFound(f'Inspection report for ID {report_id} not found')

    def get(self, request, report_id):
        report = self.get_object(report_id)
        queryset = ReportObservation.objects.filter(report=report)

        filtered_queryset = self.filter_queryset(queryset=queryset)
        queryset = self.paginator.paginate_queryset(filtered_queryset, request)
        serializer = ObservationSerializer(queryset, many=True)
        
        return self.paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = ObservationDetailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ObservationDetailView(APIView):
    permission_classes = (IsAuthenticated, IsObsOwner)
    def get_object(self, obs_id):
        try:
            obs = ReportObservation.objects.get(id=obs_id)
            self.check_object_permissions(self.request, obs)
            return obs
        except ReportObservation.DoesNotExist:
            raise NotFound(f'Observation for ID {obs_id} not found')
        
    def get(self, request, obs_id):
        obs = self.get_object(obs_id)
        serializer = ObservationReadSerializer(obs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, obs_id):
        obs = self.get_object(obs_id)
        serializer = ObservationDetailSerializer(obs, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, obs_id):
        obs = self.get_object(obs_id)
        obs.delete()
        return Response(f'Division field object deleted for given id: {obs_id}', status=status.HTTP_204_NO_CONTENT)


class ObservationEvidenceAPIView(APIView):
    permission_classes = (IsAuthenticated, IsObsOwner)

    def get_object(self, obs_id):
        try:
            obs = ReportObservation.objects.get(id=obs_id)
            self.check_object_permissions(self.request, obs)
            return obs
        except ReportObservation.DoesNotExist:
            raise NotFound(f'Observation for ID {obs_id} not found')
        
    def get(self, request, obs_id):
        obs = self.get_object(obs_id)
        serializer = ObservationEvidenceSerializer(obs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ObservationEvidenceSerializer(request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObservationEvidenceDetailView(APIView):
    def get_object(self, evd_id):
        try:
            evidence = ObservationEvidence.objects.get(id=evd_id)
            self.check_object_permissions(self.request, evidence)
            return evidence
        except ReportObservation.DoesNotExist:
            raise NotFound(f'Observation evidence for ID {evd_id} not found')
    
    def get(self, request, evd_id):
        evidence = self.get_object(evd_id)
        serializer = ObservationEvidenceSerializer(evidence)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, evd_id):
        evidence = self.get_object(evd_id)
        serializer = ObservationEvidenceSerializer(evidence, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, evd_id):
        evidence = self.get_object(evd_id)
        evidence.delete()
        return Response(f'Division field object deleted for given id: {evd_id}', status=status.HTTP_204_NO_CONTENT)