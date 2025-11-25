from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Therapist

def therapist_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            therapist = Therapist.objects.get(email=email)
        except Therapist.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("therapist-login")

        if not check_password(password, therapist.password):
            messages.error(request, "Invalid email or password")
            return redirect("therapist-login")

        # ✅ Store therapist session manually
        request.session["therapist_id"] = therapist.id

        return redirect("therapist-dashboard")

    return render(request, "therapist/therapist_login.html")


def therapist_dashboard(request):
    if "therapist_id" not in request.session:
        return redirect("therapist_login")

    therapist = Therapist.objects.get(id=request.session["therapist_id"])
    return render(request, "therapist/dashboard.html", {"therapist": therapist})


def therapist_logout(request):
    request.session.flush()
    return redirect("therapist-login")
