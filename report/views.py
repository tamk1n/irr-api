from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
import logging

logger = logging.getLogger(__name__)

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
        response['status'] = ObservationStatusSerializer(statuses, many=True).data
        logger.critical("Platform is running at risk")
        return Response(response, status=status.HTTP_200_OK)


class CreateObservationAPIView(CreateAPIView):
    serializer_class = CreateObservationSerializer


class CreateReportAPIView(CreateAPIView):
    serializer_class = CreateReportSerializer



