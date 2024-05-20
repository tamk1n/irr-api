from django.db import models
from users.models import BaseModel


class Company(BaseModel):
    name = models.CharField(max_length=155)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Division(BaseModel):
    name = models.CharField(max_length=155)
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='divisions')

    def __str__(self):
        return self.name


class DivisionField(BaseModel):
    name = models.CharField(max_length=155)
    description = models.TextField(null=True, blank=True)
    division = models.ForeignKey('Division', on_delete=models.CASCADE, related_name='fields')

    def __str__(self):
        return self.name
