from django.contrib import admin
from .models import Company, Division, DivisionField


admin.site.register(Company)
admin.site.register(Division)
admin.site.register(DivisionField)