from django.db import models
from django.contrib.auth.models import User
from therapist.models import Therapist, Therapy
from django.conf import settings



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

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User
from therapist.models import Therapist, Therapy

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.patient.username} - {self.therapy.name}"
