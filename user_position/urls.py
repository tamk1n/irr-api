from django.urls import path
from .views import *

urlpatterns = [
    path('', UserPositionAPIView.as_view(), name='UserPositionAPIView'),
    path('<int:id>/', UserPositionDetailView.as_view(), name='UserPositionDetailView'),
]