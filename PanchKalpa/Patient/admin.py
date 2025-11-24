from django.contrib import admin
from .models import PatientProfile, Appointment

admin.site.register(PatientProfile)
admin.site.register(Appointment)
