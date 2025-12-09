from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail

from Patient.models import PatientProfile
from therapist.models import Therapist
from .models import OTP

import random


# ---------------- LANDING PAGE ---------------- #
def landing_page(request):
    return render(request, 'landing.html')


# ---------------- LOGOUT ---------------- #
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out. See you again soon!")
    return redirect("/")


# ---------------- THERAPIST SIGNUP STOPPER ---------------- #
def therapist_signup(request):
    messages.error(request, "Therapist can be added only by admin!")
    return redirect("signup")


# ---------------- SIGNUP (Only Patient Can Sign Up) ---------------- #
def signup_view(request):
    if request.method == "POST":
        role = request.POST.get("role")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=full_name
        )

        if role == "patient":
            PatientProfile.objects.create(
                user=user,
                contact=request.POST.get("contact"),
                age=request.POST.get("age"),
                dob=request.POST.get("dob"),
                gender=request.POST.get("gender"),
                address=request.POST.get("address"),
                allergies=request.POST.get("allergies")
            )

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "accounts/login.html")



# ==========================  OTP LOGIN SYSTEM  =========================== #

# ---- Step 1: Send OTP via Email ---- #
def send_otp(request):
    import json
    data = json.loads(request.body)
    email = data["email"]

    user = User.objects.filter(email=email).first()
    if not user:
        return JsonResponse({"status": "error", "message": "Email not registered!"})

    otp = str(random.randint(100000, 999999))
    OTP.objects.update_or_create(user=user, defaults={"code": otp})

    send_mail(
        subject="Your Panchkalpa Login OTP",
        message=f"Your OTP for login is: {otp}",
        from_email="noreply@panchkalpa.com",
        recipient_list=[email],
    )

    return JsonResponse({"status": "sent"})


# ---- Step 2: Verify OTP & Login ---- #
def otp_login(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")   # ✔ correct template

    email = request.POST.get("identifier")
    otp_input = request.POST.get("otp")

    user = User.objects.filter(email=email).first()
    otp_obj = OTP.objects.filter(user=user).first()

    if not otp_obj:
        messages.error(request, "OTP not generated yet")
        return redirect("login")

    if otp_obj.is_expired():
        otp_obj.delete()
        messages.error(request, "OTP expired, please request again")
        return redirect("login")

    if otp_obj.code == otp_input:
        login(request, user)
        otp_obj.delete()

        # Therapist or Patient redirection
        if Therapist.objects.filter(email=email).exists():
            return redirect("therapist-dashboard")
        return redirect("patient-dashboard")

    messages.error(request, "Invalid OTP")
    return redirect("login")
