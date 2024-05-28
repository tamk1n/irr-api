from django.urls import path
from .views import *

urlpatterns = [
    path('', CompanyAPIView.as_view(), name='CompanyAPIView'),
    path('divisions/', DivisionAPIView.as_view(), name='DivisionAPIViewGET'),
    path('divisions/<int:division_id>/', DivisionDetailView.as_view(), name='DivisionDetailView'),
    path('divisions/fields/', DivisionFieldAPIView.as_view(), name='DivisionFieldAPIView'),
    path('divisions/<int:division_id>/fields/', DivisionFieldAPIView.as_view(), name='DivisionFieldAPIView'),
    path('divisions/<int:division_id>/fields/<int:field_id>/', DivisionFieldDetailView.as_view(), name='DivisionFieldDetailView')
]