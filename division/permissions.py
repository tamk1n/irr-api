from rest_framework import permissions
from user_position.models import *

class IsUserManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.position == UserPosition.objects.first()