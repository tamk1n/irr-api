from django.urls import path
from .views import *

urlpatterns = [
    path('static-data/', ObservationStaticDataAPIView.as_view(), name='ObservationStaticDataAPIView'),
    path('', ReportAPIView.as_view(), name='ReportAPIView')
]