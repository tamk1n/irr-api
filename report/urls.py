from django.urls import path
from .views import *

urlpatterns = [
    path('static-data/', ObservationStaticDataAPIView.as_view(), name='ObservationStaticDataAPIView'),
    path('', CreateReportAPIView.as_view(), name='CreateReportAPIView'),
    # path('<int:id>', )
    path('observation/', CreateObservationAPIView.as_view(), name='CreateObservationAPIView')

]