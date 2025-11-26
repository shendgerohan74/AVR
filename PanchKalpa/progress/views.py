from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import SessionNote, DailyProgress
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def progress_chart_data(request):
    notes = SessionNote.objects.filter(
        patient=request.user,
        recovery_score__isnull=False
    ).order_by("-created_at")[:6]

    # oldest → newest for smooth chart
    notes = list(reversed(notes))

    labels = [n.created_at.strftime("%b %d") for n in notes]
    scores = [n.recovery_score for n in notes]

    return JsonResponse({
        "labels": labels,
        "scores": scores
    })


@login_required
def progress_page(request):
    return render(request, "progress/progress.html")


@csrf_exempt
@login_required
def save_daily_log(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    data = json.loads(request.body)

    DailyProgress.objects.create(
        patient=request.user,
        pain=data.get("pain"),
        stress=data.get("stress"),
        sleep=data.get("sleep"),
    )

    return JsonResponse({"status": "success"})


@login_required
def get_progress(request):
    logs = DailyProgress.objects.filter(patient=request.user).order_by("date")

    labels = [log.date.strftime("%d %b") for log in logs]
    pain_scores = [log.pain or 0 for log in logs]
    stress_scores = [log.stress or 0 for log in logs]
    sleep_scores = [log.sleep or 0 for log in logs]

    latest = logs.last()

    return JsonResponse({
        "patient_daily": {
            "labels": labels,
            "pain": pain_scores,
            "stress": stress_scores,
            "sleep": sleep_scores
        },
        "therapist_session": {
            "date": latest.date.strftime("%d %b %Y") if latest else None,
            "mobility_score": getattr(latest, "mobility", None),
            "pain_score": getattr(latest, "therapist_pain", None),
            "remark": getattr(latest, "remark", None),
        },
        "report": {
            "last_updated": latest.date.strftime("%d %b %Y") if latest else None,
            "summary": "Report generated based on recent logs." if latest else None
        }
    })
