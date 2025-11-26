from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator

from .models import Therapist

def therapist_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check therapist existence
        try:
            therapist = Therapist.objects.get(email=email)
        except Therapist.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("therapist_login")

        # Check password
        if not check_password(password, therapist.password):
            messages.error(request, "Invalid email or password")
            return redirect("therapist_login")

        # ✅ Store therapist session
        request.session["therapist_id"] = therapist.id

        return redirect("therapist_dashboard")

    return render(request, "therapist/therapist_login.html")


def therapist_required(view_func):
    def wrapper(request, *args, **kwargs):
        if "therapist_id" not in request.session:
            return redirect("therapist_login")
        return view_func(request, *args, **kwargs)
    return wrapper


@therapist_required
def therapist_dashboard(request):
    therapist = Therapist.objects.get(id=request.session["therapist_id"])
    return render(request, "therapist-portal/dashboard.html", {"therapist": therapist})


@therapist_required
def therapist_patients(request):
    therapist = Therapist.objects.get(id=request.session["therapist_id"])
    # TODO: link actual patient data later
    return render(request, "therapist/patients.html")


@therapist_required
def session_entry(request):
    return render(request, "therapist/session_entry.html")


@therapist_required
def therapist_inventory(request):
    return render(request, "therapist/inventory.html")


@therapist_required
def therapist_reports(request):
    return render(request, "therapist/reports.html")


@therapist_required
def therapist_teleconsult(request):
    return render(request, "therapist/teleconsult.html")


def therapist_logout(request):
    request.session.flush()
    return redirect("therapist_login")
