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

    def __str__(self):
        return self.user.username
