from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from Patient.models import PatientProfile
from therapist.models import Therapist  



# LANDING PAGE 
def landing_page(request):
    return render(request, 'landing.html')

# LOGOUT VIEW
def logout_view(request):
    logout(request)
    messages.success(request, "You have succesfully logged out See you Again Soon ....!!!!")
    return redirect("/")

# Therapist signup Stopper
def therapist_signup(request):
    return messages.error(request, "Therapist can be added only by admin..!!")

#  SIGNUP PAGE 
def signup_view(request):
    if request.method == "POST":
        role = request.POST.get("role")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Check passwords
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        # Check email exists?
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup")

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=full_name
        )

        # --- PATIENT EXTRA DETAILS ---
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

        # --- THERAPIST FUTURE CODE (if needed) ---
        # elif role == "therapist":
        #     TherapistProfile.objects.create(...)

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "accounts/login.html")

def login_view(request):
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        # ✅ Authenticate by email
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')

        user = authenticate(username=user_obj.username, password=password)

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        login(request, user)

        # ✅ CHECK THERAPIST USING THERAPIST TABLE
        if Therapist.objects.filter(email=email).exists():
            return redirect("therapist-dashboard")

        # ✅ OTHERWISE PATIENT
        return redirect("patient-dashboard")

    return render(request, "accounts/login.html")


# Therapists Login

def therapist_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)

        if user is None or not hasattr(user, 'therapistprofile'):
            messages.error(request, "Invalid therapist credentials")
            return redirect("therapist-login")

        login(request, user)
        return redirect("therapist-dashboard")

    return render(request, "therapist/therapist_login.html")
