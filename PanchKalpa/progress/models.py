from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from datetime import date
from django.db import models
from django.conf import settings
from therapist.models import Therapist
from django.contrib.auth.models import User


@login_required
def save_daily_log(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Prevent duplicate entries for same day
    entry, created = DailyProgress.objects.get_or_create(
        patient=request.user,
        date=date.today()
    )

    entry.pain = data.get("pain")
    entry.stress = data.get("stress")
    entry.sleep = data.get("sleep")
    entry.save()

    return JsonResponse({"status": "success"}, status=200)


@login_required
def get_progress(request):
    logs = DailyProgress.objects.filter(patient=request.user).order_by("date")

    labels = [log.date.strftime("%d %b") for log in logs]
    pain_scores = [log.pain or 0 for log in logs]
    stress_scores = [log.stress or 0 for log in logs]
    sleep_scores = [log.sleep or 0 for log in logs]

    # Latest therapist session from SessionNote
    session = SessionNote.objects.filter(patient=request.user).first()

    return JsonResponse({
        "patient_daily": {
            "labels": labels,
            "pain": pain_scores,
            "stress": stress_scores,
            "sleep": sleep_scores
        },
        "therapist_session": {
            "date": session.created_at.strftime("%d %b %Y") if session else None,
            "mobility_score": session.recovery_score if session else None,
            "pain_score": None,  # No such field in model
            "remark": session.note if session else None,
        },
        "report": {
            "last_updated": labels[-1] if labels else None,
            "summary": "Report generated based on recent logs." if labels else None
        }
    })



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
