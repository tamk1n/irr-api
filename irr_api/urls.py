"""
URL configuration for irr_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from auth.views import UserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/token/', UserLoginView.as_view(), name='access-token'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('api/v1/', include([
        path('users/', include('users.urls')),
        path('auth/', include('auth.urls')),
        path('user-position/', include('user_position.urls')),
        path('report/', include('report.urls')),
        path('company/', include('division.urls')),
    ]))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
