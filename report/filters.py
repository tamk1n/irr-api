from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework.filters import SearchFilter
from .models import *


class ReportFilter(filters.FilterSet):
    observations_count = filters.NumberFilter(field_name='observations_count',
                                              method='filter_by_observations_count')
    observations_count__gte = filters.NumberFilter(field_name='observations_count__gte', 
                                                   lookup_expr='gte', 
                                                   method='filter_by_observations_count')
    observations_count__lte = filters.NumberFilter(field_name='observations_count__lte', 
                                                   lookup_expr='lte', 
                                                   method='filter_by_observations_count')
    issue_date = filters.DateFromToRangeFilter()

    class Meta:
        model = InspectionReport
        fields = {
            'project': ['exact', 'icontains'],
            'division__name': ['exact'],
            'field__name': ['exact'],
            'issued_by__first_name': ['exact', 'icontains'],
            'responsible_person': ['exact', 'icontains'],
            'issue_date': ['exact'],
        }

    def filter_by_observations_count(self, queryset, name, value):
        queryset = queryset.annotate(observations_count=Count('observations'))
        fields = self.get_fields()

        if name == 'observations_count':
            return queryset.filter(observations_count=value)
        elif name == 'observations_count__gte':
            return queryset.filter(observations_count__gte=value)
        elif name == 'observations_count__lte':
            return queryset.filter(observations_count__lte=value)
        else:
            return queryset


class ObservationFilter(filters.FilterSet):
    observations_count = filters.NumberFilter(field_name='observations_count',
                                              method='filter_by_observations_count')
    observations_count__gte = filters.NumberFilter(field_name='observations_count__gte', 
                                                   lookup_expr='gte', 
                                                   method='filter_by_observations_count')
    observations_count__lte = filters.NumberFilter(field_name='observations_count__lte', 
                                                   lookup_expr='lte', 
                                                   method='filter_by_observations_count')
    deadline = filters.DateFromToRangeFilter()
    close_date = filters.DateFromToRangeFilter()

    class Meta:
        model = ReportObservation
        fields = {
            'reference_doc': ['exact', 'icontains'],
            'category__name': ['exact'],
            'factor__name': ['exact'],
            'type__name': ['exact'],
            'status__name': ['exact'],
            'deadline': ['exact'],
            'close_date': ['exact']
        }

    def filter_by_observations_count(self, queryset, name, value):
        queryset = queryset.annotate(observations_count=Count('observations'))
        fields = self.get_fields()

        if name == 'observations_count':
            return queryset.filter(observations_count=value)
        elif name == 'observations_count__gte':
            return queryset.filter(observations_count__gte=value)
        elif name == 'observations_count__lte':
            return queryset.filter(observations_count__lte=value)
        else:
            return queryset
