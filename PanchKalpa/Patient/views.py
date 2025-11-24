from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Patient.models import PatientProfile   # FIXED APP NAME

def dashboard(request):
    return render(request, "patient-portal/dashboard.html")

def appointments(request):
    return render(request, "patient-portal/appointments.html")

def billing(request):
    return render(request, "patient-portal/billing.html")

@login_required
def profile(request):

    try:
        patient = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        patient = None

    context = {
        "patient": patient
    }

    return render(request, "patient-portal/profile.html", context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)

        profile = PatientProfile.objects.get(user=request.user)

        # Update User model
        profile.user.first_name = data.get("first_name", profile.user.first_name)
        profile.user.last_name = data.get("last_name", profile.user.last_name)
        profile.user.email = data.get("email", profile.user.email)
        profile.user.save()

        # Age fix: convert safe
        age = data.get("age")
        profile.age = int(age) if age not in ["", None] else None

        # Other fields
        profile.gender = data.get("gender", profile.gender)
        profile.contact = data.get("contact", profile.contact)
        profile.allergies = data.get("allergies", profile.allergies)
        profile.save()

        return JsonResponse({"status": "success"})



def teleconsult(request):
    return render(request, "patient-portal/teleconsult.html")

def progress(request):
    return render(request, "patient-portal/progress.html")
