from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import SessionNote
from django.shortcuts import render


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

