import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import DailyProgress, SessionNote   # adjust import if path differs
import json

@login_required
def get_progress(request):
    # --------------------------
    # DAILY SELF-CHECK (for graphs)
    # --------------------------
    logs = DailyProgress.objects.filter(patient=request.user).order_by("date")

    labels = [log.date.strftime("%d %b") for log in logs]
    pain_scores = [log.pain or 0 for log in logs]
    stress_scores = [log.stress or 0 for log in logs]
    sleep_scores = [log.sleep or 0 for log in logs]

    # --------------------------
    # THERAPIST SESSIONS
    # --------------------------
    latest_session = SessionNote.objects.filter(patient=request.user).first()
    all_sessions = SessionNote.objects.filter(patient=request.user).order_by("-created_at")

    # --------------------------
    # BUILD N8N REPORT PAYLOAD
    # --------------------------
    session_reports = []

    for s in all_sessions:
        session_reports.append({
            "date": s.created_at.strftime("%Y-%m-%d"),
            "pain_before": pain_scores[-2] if len(pain_scores) >= 2 else 5,   # fallback
            "pain_after": (10 - int((s.recovery_score or 50) / 10)),          # rough conversion
            "symptoms": s.note or "No symptoms recorded",
            "notes": s.note or "No therapist notes"
        })

    # --------------------------
    # CALL N8N WORKFLOW
    # --------------------------
    n8n_url = "https://shendgerohan33.app.n8n.cloud/webhook/ai-chart"

    ai_output = {
        "summary": "AI analysis unavailable",
        "improvements": [],
        "worsening": [],
        "patterns": [],
        "red_flags": [],
        "recommendations": [],
        "next_steps": [],
        "last_updated": None
    }

    try:
        print("🚀 Calling N8N now...")
        print("URL:", n8n_url)
        print("Payload:", {
            "patient_name": request.user.username,
            "reports": session_reports
        })
    
        resp = requests.post(n8n_url, json={
            "patient_name": request.user.username,
            "reports": session_reports
        }, timeout=100)
    
        print("N8N STATUS:", resp.status_code)
        print("N8N RAW RESPONSE:", resp.text)
    
        if resp.status_code == 200:
            ai_output = resp.json()
    
    except Exception as e:
        print("🔥 N8N ERROR:", e)
    

    # --------------------------
    # FINAL RESPONSE BACK TO FRONTEND
    # --------------------------
    return JsonResponse({
        "patient_daily": {
            "labels": labels,
            "pain": pain_scores,
            "stress": stress_scores,
            "sleep": sleep_scores
        },
        "therapist_session": {
            "date": latest_session.created_at.strftime("%d %b %Y") if latest_session else "--",
            "mobility_score": latest_session.recovery_score if latest_session else None,
            "pain_score": None,   # not present in your model
            "remark": latest_session.note if latest_session else None,
        },
        "report": ai_output
    })


@login_required
def save_daily_log(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        DailyProgress.objects.create(
            patient=request.user,
            pain=int(data.get("pain") or 0),
            stress=int(data.get("stress") or 0),
            sleep=int(data.get("sleep") or 0),
        )
    except Exception as e:
        # Print real error so you stop debugging blind
        print("🔥 DAILY LOG SAVE ERROR:", e)
        return JsonResponse({"error": "Server error"}, status=500)

    return JsonResponse({"status": "success"}, status=200)
