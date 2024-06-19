from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='UserRegisterView'),
    path('add-employee/', AddEmployeeView.as_view(), name='AddEmployeeView'),
    path('add-employee/<uuid:token>', RegisterEmployee.as_view(), name='RegisterEmployee'),
    path('otp/', SendOTPAPIView.as_view(), name='SendOTPAPIView'),
    path('otp/<str:otp>', InvalidateOTPView.as_view(), name='InvalidateOTPView'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='ResetPasswordAPIView')
]