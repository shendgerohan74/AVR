from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from Patient.models import PatientProfile, Appointment
from therapist.models import Therapist, Therapy

# ------------------ Dashboard ------------------
@login_required
def dashboard(request):
    # Get ALL upcoming appointments
    upcoming = Appointment.objects.filter(
        patient=request.user
    ).order_by("date", "time")

    return render(request, "patient-portal/dashboard.html", {
        "upcoming": upcoming
    })


# ------------------ Appointments ------------------
@login_required
def appointments(request):
    therapies = Therapy.objects.all()
    therapists = Therapist.objects.all()

    if request.method == "POST":
        therapy_id = request.POST.get("therapy")
        therapist_id = request.POST.get("therapist")
        date = request.POST.get("date")
        time = request.POST.get("time")

        Appointment.objects.create(
            patient=request.user,
            therapy_id=therapy_id,
            therapist_id=therapist_id,
            date=date,
            time=time
        )

        return redirect("patient-appointments")

    upcoming = Appointment.objects.filter(patient=request.user).order_by("date")

    return render(request, "patient-portal/appointments.html", {
        "therapies": therapies,
        "therapists": therapists,
        "upcoming": upcoming,
    })


# ------------------ Profile PAGE ------------------
@login_required
def profile(request):
    patient = PatientProfile.objects.get(user=request.user)
    return render(request, "patient-portal/profile.html", {
        "patient": patient
    })


# ------------------ Profile UPDATE API ------------------
@login_required
def update_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)

        profile = PatientProfile.objects.get(user=request.user)

        # Update User basic details
        profile.user.first_name = data.get("first_name", profile.user.first_name)
        profile.user.last_name = data.get("last_name", profile.user.last_name)
        profile.user.email = data.get("email", profile.user.email)
        profile.user.save()

        # Update age safely
        age = data.get("age")
        profile.age = int(age) if age not in ["", None] else None

        # Update other fields
        profile.gender = data.get("gender", profile.gender)
        profile.contact = data.get("contact", profile.contact)
        profile.allergies = data.get("allergies", profile.allergies)
        profile.save()

        return JsonResponse({"status": "success"})


# ------------------ Other Pages ------------------
def teleconsult(request):
    return render(request, "patient-portal/teleconsult.html")


def progress(request):
    return render(request, "patient-portal/progress.html")


# def billing(request):
#     return render(request, "patient-portal/billing.html")
