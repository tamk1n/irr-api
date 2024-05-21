from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import *

@receiver(pre_save, sender=ReportObservation)
def updating_license(sender, instance, created, **kwargs):
    if instance.close_date:
        instance.is_active = False
        instance.status = ObservationStatus.objects.get('Bağlı')




