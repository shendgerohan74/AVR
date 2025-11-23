from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, "patient-portal/dashboard.html")

def appointments(request):
    return render(request, "patient-portal/appointments.html")

def billing(request):
    return render(request, "patient-portal/billing.html")

def profile(request):
    return render(request, "patient-portal/profile.html")

def teleconsult(request):
    return render(request, "patient-portal/teleconsult.html")

def progress(request):
    return render(request, "patient-portal/progress.html")