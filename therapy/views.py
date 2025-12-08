from django.shortcuts import render, get_object_or_404
from .models import Therapy

def therapy_detail(request, therapy_id):
    therapy = get_object_or_404(Therapy, id=therapy_id)

    # Add therapy suggestions here
    suggestions = [
        "Follow light, easily digestible diet for at least 2 days",
        "Avoid heavy, oily, fried food",
        "Sleep well the previous night",
        "Drink warm water regularly",
        "Follow physician’s instructions on internal oleation (Snehapana)",
        "Report any digestive discomfort before therapy"
    ]

    context = {
        'therapy': therapy,
        'suggestions': suggestions
    }
    return render(request, 'patient_dashboard.html', context)
