from django.db import models
from django.contrib.auth.models import User
from therapist.models import Therapist, Therapy
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User




class PatientProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="patientprofile"
    )

    contact = models.CharField(max_length=15, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    allergies = models.CharField(max_length=255, null=True, blank=True)
    prakriti_type = models.CharField(max_length=20, null=True, blank=True)
    therapy_stage = models.CharField(max_length=20, null=True, blank=True)  
    symptoms = models.JSONField(default=list, blank=True)
    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.patient.user.username} - {self.therapy.name}"
        


from django.db import models

# Patient/models.py
class ConsentForm(models.Model):
    patient_name = models.CharField(max_length=200)
    age = models.IntegerField()
    contact = models.CharField(max_length=15)
    therapy_name = models.CharField(max_length=100)
    therapy_description = models.TextField()
    understood_risks = models.BooleanField()
    voluntary = models.BooleanField()
    notes = models.TextField(blank=True, null=True)
    signature = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
