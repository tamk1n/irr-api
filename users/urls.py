from django.urls import path
from .views import *

urlpatterns = [
    path('', UserAPIView.as_view(), name='UserAPIView'),
]