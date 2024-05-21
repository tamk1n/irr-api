from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, date

from users.models import BaseModel


class InspectionReport(BaseModel):
    project = models.TextField()
    division = models.ForeignKey('division.Division', on_delete=models.CASCADE, related_name='reports')
    field = models.ForeignKey('division.DivisionField', on_delete=models.CASCADE, related_name='reports')
    issued_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='observations')
    responsible_person = models.CharField(max_length=155)
    issue_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'IR Number {self.id}'


class ReportObservation(BaseModel):
    report = models.ForeignKey('InspectionReport', on_delete=models.CASCADE, related_name='observations')
    content = models.TextField()
    reference_doc = models.CharField(max_length=155)
    category = models.ForeignKey('ObservationCategory', on_delete=models.CASCADE, related_name='observations')
    factor = models.ForeignKey('ObservationFactor', on_delete=models.CASCADE, related_name='observations')
    type = models.ForeignKey('ObservationType', on_delete=models.CASCADE, related_name='observations')
    status = models.ForeignKey('ObservationStatus', on_delete=models.CASCADE, related_name='observations')
    action = models.TextField()
    deadline = models.DateField()
    close_date = models.DateField(blank=True, null=True)

    def clean(self):
        if self.close_date and self.close_date > date.today():
            raise ValidationError('You cannot define close date in future.')

        if self.close_date and self.close_date < self.report.issue_date:
            raise ValidationError('Close date cannot be prior to issue date.')

        return super().clean()

    def __str__(self):
        return self.report.__str__() + 'Obs' + self.id


class ObservationType(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ObservationFactor(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ObservationCategory(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ObservationStatus(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


def evidences_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/IR_<report_id>/Obs_<observation_id>/filename
    return "IR_{0}/Obs_{1}/{2}".format(instance.observation.report.id, instance.observation.id, filename)


class ObservationEvidence(BaseModel):
    observation = models.ForeignKey('ReportObservation', on_delete=models.CASCADE, related_name='evidences')
    evidence = models.ImageField(upload_to=evidences_path)

