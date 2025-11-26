# 



# therapist/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Therapist

# ---------------------- LOGIN ----------------------

def therapist_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check therapist exists
        try:
            therapist = Therapist.objects.get(email=email)
        except Therapist.DoesNotExist:
            return render(request, "therapist/therapist_login.html", {
                "error": "Therapist not found"
            })

        # Check password
        if not check_password(password, therapist.password):
            return render(request, "therapist/therapist_login.html", {
                "error": "Incorrect password"
            })

        # SUCCESS: store session
        request.session["therapist_id"] = therapist.id
        return redirect("therapist_dashboard")

    return render(request, "therapist/therapist_login.html")


# ---------------------- MIDDLEWARE ----------------------

def therapist_required(view_func):
    def wrapper(request, *args, **kwargs):
        if "therapist_id" not in request.session:
            return redirect("therapist_login")
        return view_func(request, *args, **kwargs)
    return wrapper


# ---------------------- DASHBOARD ----------------------

@therapist_required
def therapist_dashboard(request):
    therapist = Therapist.objects.get(id=request.session["therapist_id"])
    return render(request, "therapist-portal/dashboard.html", {"therapist": therapist})


# ---------------------- OTHER PAGES ----------------------

@therapist_required
def therapist_patients(request):
    return render(request, "therapist-portal/patients.html")


@therapist_required
def session_entry(request):
    return render(request, "therapist-portal/session.html")


@therapist_required
def therapist_inventory(request):
    return render(request, "therapist-portal/inventory.html")


@therapist_required
def therapist_reports(request):
    return render(request, "therapist-portal/reports.html")


@therapist_required
def therapist_teleconsult(request):
    return render(request, "therapist-portal/teleconsult.html")
