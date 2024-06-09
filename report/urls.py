from django.urls import path, include
from .views import *

urlpatterns = [
    path('static-data/', ObservationStaticDataAPIView.as_view(), name='ObservationStaticDataAPIView'),
    path('', ReportAPIView.as_view(), name='ReportAPIView'),

    path('<int:report_id>/', include([
        path('', ReportDetailView.as_view(), name='ReportDetailView'),
        path('observations/', ObservationAPIView.as_view(), name='ObservationAPIView'),
    ])),

    path('observations/', include([
        path('', ObservationAPIView.as_view(), name='ObservationAPIView'),
        path('<int:obs_id>', ObservationDetailView.as_view(), name='ObservationDetailView'),
        path('<int:obs_id>/evidences/', ObservationEvidenceAPIView.as_view(), name='ObservationDetailView'),
    ])),
    path('evidence/', ObservationEvidenceAPIView.as_view(), name='ObservationDetailView'),
    path('evidence/<int:evd_id>', ObservationEvidenceDetailView.as_view(), name='ObservationEvidenceDetailView')
    
    

]