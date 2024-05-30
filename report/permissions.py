from rest_framework import permissions
from user_position.models import *
from .models import *


class IsReportOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.issued_by == request.user or request.user.position == request.user.is_manager
    

class IsObsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == 'POST':
            if report_id := request.data.get('report'):
                if report := InspectionReport.objects.filter(id=report_id).first():
                    return report.issued_by == request.user or request.user.is_manager
            
            if obs_id := request.data.get('observation'):
                if obs := ReportObservation.objects.filter(id=obs_id).first():
                    return obs.report.issued_by == request.user or request.user.is_manager
            
        return True

        
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.report.issued_by == request.user or request.user.is_manager