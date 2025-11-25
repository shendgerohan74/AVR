from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Therapist

def therapist_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            therapist = Therapist.objects.get(email=email)
        except Therapist.DoesNotExist:
            return render(request, "accounts/therapist_login.html", {
                "error": "Therapist not found"
            })

        if not check_password(password, therapist.password):
            return render(request, "accounts/therapist_login.html", {
                "error": "Incorrect password"
            })

        request.session["therapist_id"] = therapist.id
        return redirect("therapist_dashboard")

    return render(request, "accounts/therapist_login.html")





def therapist_dashboard(request):
    therapist_id = request.session.get("therapist_id")
    if not therapist_id:
        return redirect("therapist_login")

    therapist = Therapist.objects.get(id=therapist_id)

    return render(request, "therapist-portal/dashboard.html", {
        "therapist": therapist
    })

def therapist_teleconsult(request):
    therapist_id = request.session.get("therapist_id")
    if not therapist_id:
        return redirect("therapist_login")
    therapist = Therapist.objects.get(id=therapist_id)
    return render(request, "therapist-portal/teleconsult.html", {"therapist": therapist})



# Create your views here.
def therapist_patients(request):
    return render(request, "therapist-portal/patients.html")

def session_entry(request):
    return render(request, "therapist-portal/session.html")

def therapist_inventory(request):
    return render(request, "therapist-portal/inventory.html")

def therapist_reports(request):
    return render(request, "therapist-portal/reports.html")
def therapist_reports(request):
    return render(request, "therapist-portal/teleconsult.html")
