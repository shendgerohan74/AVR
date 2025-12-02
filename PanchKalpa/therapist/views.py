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





from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.conf import settings
import os
from datetime import datetime

from .models import Therapist, SessionNote


def generate_pdf(template_path, context, output_file):
    html = render_to_string(template_path, context)
    with open(output_file, "wb+") as pdf:
        pisa.CreatePDF(html, dest=pdf)


from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
from datetime import datetime
from io import BytesIO

def save_session(request):
    if request.method == "POST":
        # Fetch form data
        patient_name = request.POST.get("patient_name")
        therapy_name = request.POST.get("therapy_name")
        notes = request.POST.get("notes")
        inventory_item = request.POST.get("inventory_item")
        inventory_qty = request.POST.get("inventory_qty")
        
        html = render_to_string("pdf/session_template.html", {
            "patient_name": patient_name,
            "therapy_name": therapy_name,
            "notes": notes,
            "inventory_item": inventory_item,
            "inventory_qty": inventory_qty,
            "generated_on": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
        })

        # ------------------------------------------------------------------
        #  CREATE PDF IN MEMORY
        # ------------------------------------------------------------------
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        y = 800

        p.setFont("Helvetica-Bold", 18)
        p.drawString(180, y, "PanchKalpa - Session Report")
        y -= 40

        p.setFont("Helvetica", 12)
        date_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        p.drawString(50, y, f"Generated On: {date_str}")
        y -= 30

        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Patient Name:")
        p.setFont("Helvetica", 12)
        p.drawString(160, y, patient_name)
        y -= 30

        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Therapy Performed:")
        p.setFont("Helvetica", 12)
        p.drawString(200, y, therapy_name)
        y -= 30

        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Inventory Used:")
        p.setFont("Helvetica", 12)
        p.drawString(170, y, f"{inventory_item} ({inventory_qty})")
        y -= 40

        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Session Notes:")
        y -= 25

        p.setFont("Helvetica", 12)

        for line in notes.split("\n"):
            p.drawString(60, y, line)
            y -= 20

        p.showPage()
        p.save()

        buffer.seek(0)

        # ------------------------------------------------------------------
        #  Return PDF as response (DOWNLOAD)
        # ------------------------------------------------------------------
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="session_report.pdf"'
        return response

    return render(request, "therapist-portal/session.html")


def session_success(request):
    return render(request, "therapist-portal/session_success.html")


from django.contrib.auth.decorators import login_required

@login_required
def session_history(request):
    therapist = Therapist.objects.get(email=request.session["email"])
    sessions = SessionNote.objects.filter(therapist=therapist).order_by("-created_at")
    return render(request, "therapist-portal/session_history.html", {"sessions": sessions})
