from django.contrib import admin
from .models import *

admin.site.register(InspectionReport)
admin.site.register(ReportObservation)
admin.site.register(ObservationType)
admin.site.register(ObservationFactor)
admin.site.register(ObservationCategory)
admin.site.register(ObservationStatus)
admin.site.register(ObservationEvidence)


