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


from django.http import JsonResponse
from .models import Center


def get_nearest_center(request):
    city = request.GET.get("city", "").strip().lower()

    if city == "":
        return JsonResponse({"error": "City is required"}, status=400)

    # City match in DB
    center = Center.objects.filter(city__iexact=city).first()

    if center:
        return JsonResponse({
            "found": True,
            "center_name": center.name,
            "city": center.city
        })

    return JsonResponse({"found": False, "message": "No center found in this city"})

from django.http import JsonResponse
from .models import Therapist

def get_doctors_by_therapy(request):
    therapy = request.GET.get("therapy", "").strip().lower()
    center = request.GET.get("center", "").strip()

    if therapy == "" or center == "":
        return JsonResponse({"error": "Therapy and Center are required"}, status=400)

    # filter doctors by center
    doctors = Therapist.objects.filter(center__name=center)

    # filter doctors by expertise text
    doctors = [doc for doc in doctors if therapy in doc.expertise.lower()]

    if not doctors:
        return JsonResponse({"found": False, "message": "No doctors found for this therapy"})

    # sort doctors by experience (descending)
    doctors_sorted = sorted(doctors, key=lambda x: x.experience, reverse=True)


    
    recommended = doctors_sorted[0]  # top experienced doctor

    other_doctors = doctors_sorted[1:]

    return JsonResponse({
        "found": True,
        "recommended": {
            "name": recommended.name,
            "experience": recommended.experience,
            "expertise": recommended.expertise,
        },
        "other_doctors": [
            {
                "name": doc.name,
                "experience": doc.experience,
                "expertise": doc.expertise
            }
            for doc in other_doctors
        ]
    })


from .models import Therapist

def get_doctors_by_center(request):
    center_name = request.GET.get("center", "").strip()

    if center_name == "":
        return JsonResponse({"error": "Center name is required"}, status=400)

    # Fetch doctors from same center
    doctors = Therapist.objects.filter(center__name=center_name)

    if not doctors:
        return JsonResponse({"found": False, "message": "No doctors found in this center"})

    # Sort by experience (descending)
    doctors_sorted = sorted(doctors, key=lambda x: x.experience, reverse=True)

    recommended = doctors_sorted[0]
    other_doctors = doctors_sorted[1:]

    return JsonResponse({
        "found": True,
        "center": center_name,
        "recommended": {
            "name": recommended.name,
            "email": recommended.email,
            "experience": recommended.experience,
            "expertise": recommended.expertise,
        },
        "other_doctors": [
            {
                "name": doc.name,
                "email": doc.email,
                "experience": doc.experience,
                "expertise": doc.expertise,
            }
            for doc in other_doctors
        ]
    })




from .models import AvailableSlot, Appointment
from django.db.models import Q

def get_available_slots(request):
    doctor_id = request.GET.get("doctor_id")
    date = request.GET.get("date")

    if not doctor_id or not date:
        return JsonResponse({"error": "Doctor ID and date are required"}, status=400)

    # Doctor ke saare slots
    all_slots = AvailableSlot.objects.filter(therapist_id=doctor_id)

    # Already booked slots (same day)
    booked = Appointment.objects.filter(
        therapist_id=doctor_id,
        date=date
    )

    booked_slots = {(b.start_time, b.end_time) for b in booked}

    # Only free slots
    free_slots = [
        {"start": str(slot.start_time), "end": str(slot.end_time)}
        for slot in all_slots
        if (slot.start_time, slot.end_time) not in booked_slots
    ]

    return JsonResponse({
        "total": len(free_slots),
        "free_slots": free_slots
    })



from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def book_appointment(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)

    data = json.loads(request.body)

    therapist_id = data.get("therapist_id")
    patient_name = data.get("patient_name")
    date = data.get("date")
    start = data.get("start_time")
    end = data.get("end_time")

    if not all([therapist_id, patient_name, date, start, end]):
        return JsonResponse({"error": "All fields are required"}, status=400)

    Appointment.objects.create(
        therapist_id=therapist_id,
        patient_name=patient_name,
        date=date,
        start_time=start,
        end_time=end
    )

    return JsonResponse({"status": "success", "message": "Appointment booked successfully"})
