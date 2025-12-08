from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Therapist

# ---------------------- THERAPIST LOGIN ----------------------

def therapist_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if therapist exists
        try:
            therapist = Therapist.objects.get(email=email)
        except Therapist.DoesNotExist:
            return render(request, "therapist/therapist_login.html", {
                "error": "Email not found"
            })

        # Check password
        if check_password(password, therapist.password):
            request.session["therapist_id"] = therapist.id
            return redirect("therapist-dashboard")   # ✔ Correct name

        return render(request, "therapist/therapist_login.html", {
            "error": "Wrong password"
        })

    return render(request, "therapist/therapist_login.html")


# ---------------------- MIDDLEWARE PROTECTOR ----------------------

def therapist_required(view_func):
    def wrapper(request, *args, **kwargs):
        if "therapist_id" not in request.session:
            return redirect("therapist-login")    # ✔ Correct name
        return view_func(request, *args, **kwargs)
    return wrapper


# ---------------------- DASHBOARD ----------------------

@therapist_required
def therapist_dashboard(request):
    user = request.user

    if not hasattr(user, "therapistprofile"):
        return redirect("not_authorized")  # or your fallback page

    therapist = user.therapistprofile

    appointments = Appointment.objects.filter(
        therapist=therapist,
        date__gte=timezone.now().date()
    ).order_by("date")

    return render(request, "therapist/dashboard.html", {
        "appointments": appointments
    })


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


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from therapist.models import Therapist
from Patient.models import Appointment, PatientProfile
from Patient.utils import notify_patient
from django.http import HttpResponseForbidden


@login_required
def therapist_send_notification(request):
    therapist = Therapist.objects.get(user=request.user)

    # All unique patients assigned to this therapist
    appointments = Appointment.objects.filter(therapist=therapist)
    patients = list({a.patient for a in appointments})  # unique + list

    if request.method == "POST":
        patient_id = request.POST.get("patient")
        title = request.POST.get("title")
        message = request.POST.get("message")

        # Prevent sending to unrelated patients (security)
        try:
            patient = PatientProfile.objects.get(id=patient_id)
        except PatientProfile.DoesNotExist:
            return HttpResponseForbidden("Invalid patient")

        if patient not in patients:
            return HttpResponseForbidden("You cannot message this patient")

        notify_patient(patient, title, message)

        return redirect("therapist-send-notification")  # reload same page

    return render(
        request,
        "therapist/send_notification.html",
        {"patients": patients}
    )
