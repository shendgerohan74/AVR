from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import SessionNote, DailyProgress
from django.shortcuts import render
import json
    

@login_required
def save_daily_log(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    DailyProgress.objects.create(
        patient=request.user,
        pain=data.get("pain"),
        stress=data.get("stress"),
        sleep=data.get("sleep"),
    )

    return JsonResponse({"status": "success"}, status=200)


@login_required
def get_progress(request):
    logs = DailyProgress.objects.filter(patient=request.user).order_by("date")

    labels = [log.date.strftime("%d %b") for log in logs]
    pain_scores = [log.pain or 0 for log in logs]
    stress_scores = [log.stress or 0 for log in logs]
    sleep_scores = [log.sleep or 0 for log in logs]

    # therapist data must come from SessionNote
    session = SessionNote.objects.filter(patient=request.user).order_by("-created_at").first()

    return JsonResponse({
        "patient_daily": {
            "labels": labels,
            "pain": pain_scores,
            "stress": stress_scores,
            "sleep": sleep_scores
        },
        "therapist_session": {
            "date": session.created_at.strftime("%d %b %Y") if session else None,
            "mobility_score": session.mobility_score if session else None,
            "pain_score": session.pain_score if session else None,
            "remark": session.remark if session else None,
        },
        "report": {
            "last_updated": labels[-1] if labels else None,
            "summary": "Report generated based on recent logs." if labels else None
        }
    })


@login_required
def progress_page(request):
    return render(request, "patient-portal/progress.html")