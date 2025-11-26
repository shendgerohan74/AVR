from django.db import models
from django.conf import settings
from therapist.models import Therapist
from django.contrib.auth.models import User

User = settings.AUTH_USER_MODEL

# Session Notes for dashboard

class SessionNote(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progress_notes")
    therapist = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True, blank=True)
    recovery_score = models.PositiveSmallIntegerField(null=True, blank=True)  # 0-100
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient} - {self.recovery_score}"


# Progress Page 

class DailyProgress(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    # Patient-entered values
    pain = models.IntegerField(null=True, blank=True)
    stress = models.IntegerField(null=True, blank=True)
    sleep = models.IntegerField(null=True, blank=True)

    # Therapist-entered values
    bp = models.CharField(max_length=20, null=True, blank=True)
    therapist_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient.email} - {self.date}"
