from django.db import models
from django.conf import settings
from therapist.models import Therapist

User = settings.AUTH_USER_MODEL

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
