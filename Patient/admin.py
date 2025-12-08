from django.contrib import admin
from .models import PatientProfile, Appointment, Notification

admin.site.register(PatientProfile)
admin.site.register(Appointment)
admin.site.register(Notification)