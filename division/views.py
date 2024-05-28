from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from .permissions import IsUserManager
from .serializers import *
from users.models import UserProfile

class CompanyAPIView(APIView):
    permission_classes = (IsAuthenticated, IsUserManager)

    def get_object(self, request):
        try:
            return request.user.my_profile.company
        except (Company.DoesNotExist, UserProfile.DoesNotExist):
            raise NotFound('Company not found')

    def get(self, request):
        company = self.get_object(request)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        company = self.get_object(request)
        serializer = CompanyUpdateSerializer(company, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        company = self.get_object(request)
        company.is_actve = False
        company.save()
        return Response(f'Company object deleted for given id: {company.id}', status=status.HTTP_204_NO_CONTENT)


class DivisionAPIView(APIView):
    permission_classes = (IsAuthenticated, IsUserManager)
    paginator = PageNumberPagination()

    def get_object(self, request,):
        try:
            return request.user.my_profile.company
        except (Company.DoesNotExist, UserProfile.DoesNotExist):
            raise NotFound('Company not found')

    def get(self, request):
        company = self.get_object(request)
        queryset = Division.objects.filter(company=company)
        queryset = self.paginator.paginate_queryset(queryset, request)
        serializer = DivisionSerializer(queryset, many=True)
        response = self.paginator.get_paginated_response(serializer.data)
        return response
    
    def post(self, request):
        serializer = DivisionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DivisionDetailView(APIView):
    permission_classes = (IsAuthenticated, IsUserManager)

    def get_object(self, request, division_id):
        try:
            company = request.user.my_profile.company
            obj = Division.objects.get(id=division_id, company=company, is_active=True)
            return obj
        except (Company.DoesNotExist, UserProfile.DoesNotExist):
            raise NotFound('Company not found')
        except Division.DoesNotExist:
            raise NotFound('Division not found')
        
    def get(self, request, division_id):
        obj = self.get_object(request, division_id)
        serializer = DivisionSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, division_id):
        division = self.get_object(request, division_id)
        serializer = DivisionSerializer(division, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, division_id):
        division = self.get_object(request, division_id)
        division.is_active = False
        division.save()
        return Response(f'Division object deleted for given id: {division.id}', status=status.HTTP_204_NO_CONTENT)


class DivisionFieldAPIView(APIView):
    permission_classes = (IsAuthenticated, IsUserManager)
    paginator = PageNumberPagination()

    def get_object(self, request, division_id):
        try:
            company = request.user.my_profile.company
            division = Division.objects.get(id=division_id, company=company, is_active=True)
            return division
        except (Company.DoesNotExist, UserProfile.DoesNotExist):
            raise NotFound('Company not found')
        except Division.DoesNotExist:
            raise NotFound('Division not found')
    
    def get(self, request, division_id):
        division = self.get_object(request, division_id)
        divisions = DivisionField.objects.filter(division__id=division_id, is_active=True)
        queryset = self.paginator.paginate_queryset(divisions, request)
        serializer = DivisionFieldSerializer(queryset, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = DivisionFieldSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DivisionFieldDetailView(APIView):
    def get_object(self, request, division_id, field_id):
        try:
            company = request.user.my_profile.company
            division = Division.objects.get(id=division_id, company=company, is_active=True)
            field = DivisionField.objects.get(id=field_id, division=division, is_active=True)
            return division
        except (Company.DoesNotExist, UserProfile.DoesNotExist):
            raise NotFound('Company not found')
        except Division.DoesNotExist:
            raise NotFound('Division not found')
    
    def get(self, request, division_id, field_id):
        field = self.get_object(request, division_id, field_id)
        serializer = DivisionFieldSerializer(field)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, division_id, field_id):
        field = self.get_object(request, division_id, field_id)
        serializer = DivisionFieldSerializer(field, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, division_id, field_id):
        field = self.get_object(request, division_id, field_id)
        field.is_active = False
        field.save()
        return Response(f'Division field object deleted for given id: {field.id}', status=status.HTTP_204_NO_CONTENT)
