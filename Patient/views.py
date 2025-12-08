from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.utils import timezone
from Patient.models import PatientProfile, Appointment
from therapist.models import Therapist, Therapy
from .services import generate_diet_plan   # we will create this next


# ------------------ Dashboard ------------------
@login_required
def dashboard(request):
    patient = request.user.patientprofile

    upcoming = Appointment.objects.filter(
        patient=patient,
        date__gte=timezone.now().date()
    ).order_by("date")

    history = Appointment.objects.filter(
        patient=patient,
        date__lt=timezone.now().date()
    ).order_by("-date")

    
    return render(request, "patient-portal/dashboard.html", {
        "upcoming": upcoming,
        "history": history,
        "consents": consents
    })
        

# ------------------ Appointments ------------------
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Appointment
from therapist.models import Therapist, Therapy

@login_required
def appointments(request):
    patient = request.user.patientprofile   # ✅ ALWAYS get profile first
    therapies = Therapy.objects.all()
    therapists = Therapist.objects.all()

    if request.method == "POST":
        therapy_id = request.POST.get("therapy")
        therapist_id = request.POST.get("therapist")
        date = request.POST.get("date")
        time = request.POST.get("time")

        Appointment.objects.create(
            patient=patient,              # ✅ FIXED
            therapy_id=therapy_id,
            therapist_id=therapist_id,
            date=date,
            time=time
        )

        return redirect("patient-appointments")

    upcoming = Appointment.objects.filter(
        patient=patient
    ).order_by("date")
    
    history = Appointment.objects.filter(
        patient=patient
    ).order_by("-date")

    return render(request, "patient-portal/appointments.html", {
        "therapies": therapies,
        "therapists": therapists,
        "upcoming": upcoming,
        "history": history
    })



# ------------------ Profile PAGE ------------------
@login_required
def profile(request):
    patient = PatientProfile.objects.get(user=request.user)
    return render(request, "patient-portal/profile.html", {
        "patient": patient
    })


# ------------------ Profile UPDATE API ------------------
@login_required
def update_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)

        profile = PatientProfile.objects.get(user=request.user)

        # Update User basic details
        profile.user.first_name = data.get("first_name", profile.user.first_name)
        profile.user.last_name = data.get("last_name", profile.user.last_name)
        profile.user.email = data.get("email", profile.user.email)
        profile.user.save()

        # Update age safely
        age = data.get("age")
        profile.age = int(age) if age not in ["", None] else None

        # Update other fields
        profile.gender = data.get("gender", profile.gender)
        profile.contact = data.get("contact", profile.contact)
        profile.allergies = data.get("allergies", profile.allergies)
        profile.save()

        return JsonResponse({"status": "success"})


# ------------------ Other Pages ------------------
def teleconsult(request):
    return render(request, "patient-portal/teleconsult.html")


def progress(request):
    return render(request, "patient-portal/progress.html")

def diet(request):
    return render(request, "patient-portal/diet.html")

def diet_plan_api(request):

    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        profile = PatientProfile.objects.get(user=user)
    except PatientProfile.DoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)

    if not profile.prakriti_type:
        return JsonResponse({
            "error": "Prakriti missing",
            "message": "Run Prakriti Analyzer first."
        }, status=400)

    diet = generate_diet_plan(
        prakriti=profile.prakriti_type,
        stage=profile.therapy_stage,
        symptoms=profile.symptoms
    )

    return JsonResponse(diet, safe=False)



PRAKRITI_QUESTIONS = [
    {
        "question": "What is your body frame/build?",
        "vata": "Thin, lean, hard to gain weight",
        "pitta": "Medium, well-proportioned, athletic",
        "kapha": "Heavy, broad shoulders, easy to gain weight"
    },
    {
        "question": "How is your skin texture?",
        "vata": "Dry, rough, thin with visible veins",
        "pitta": "Warm, oily, prone to rashes/acne",
        "kapha": "Thick, smooth, cool, well-moisturized"
    },
    {
        "question": "What is your hair type?",
        "vata": "Dry, brittle, thin, frizzy",
        "pitta": "Fine, oily, early graying/balding",
        "kapha": "Thick, lustrous, oily, wavy"
    },
    {
        "question": "How are your eyes?",
        "vata": "Small, dry, active, dark/brown",
        "pitta": "Sharp, penetrating, light-sensitive, green/gray",
        "kapha": "Large, calm, attractive, blue/brown"
    },
    {
        "question": "What is your appetite like?",
        "vata": "Irregular, sometimes forget to eat",
        "pitta": "Strong, get irritable if meals delayed",
        "kapha": "Steady but can skip meals easily"
    },
    {
        "question": "How is your digestion?",
        "vata": "Irregular, gas, bloating, constipation",
        "pitta": "Strong, quick, burning sensation, loose stools",
        "kapha": "Slow, heavy feeling after meals"
    },
    {
        "question": "How is your thirst?",
        "vata": "Variable, sometimes forget to drink",
        "pitta": "High, need frequent water intake",
        "kapha": "Low, can go long without water"
    },
    {
        "question": "How do you sweat?",
        "vata": "Minimal sweating, no strong odor",
        "pitta": "Profuse sweating, strong odor",
        "kapha": "Moderate, pleasant smell"
    },
    {
        "question": "How is your sleep pattern?",
        "vata": "Light, interrupted, less than 6 hours",
        "pitta": "Sound, moderate 6-7 hours",
        "kapha": "Deep, heavy, more than 8 hours"
    },
    {
        "question": "How is your mental activity?",
        "vata": "Always active, restless mind",
        "pitta": "Sharp, focused, aggressive thoughts",
        "kapha": "Calm, steady, slow to process"
    },
    {
        "question": "How do you learn?",
        "vata": "Quick to learn, quick to forget",
        "pitta": "Moderate speed, sharp memory",
        "kapha": "Slow to learn, never forget"
    },
    {
        "question": "How do you handle stress?",
        "vata": "Anxious, worried, fearful",
        "pitta": "Angry, irritable, frustrated",
        "kapha": "Calm, withdrawn, avoid confrontation"
    },
    {
        "question": "What is your emotional nature?",
        "vata": "Enthusiastic, mood changes quickly",
        "pitta": "Intense, passionate, determined",
        "kapha": "Supportive, content, possessive"
    },
    {
        "question": "How is your speech?",
        "vata": "Fast, talks a lot, changes topics",
        "pitta": "Sharp, precise, argumentative",
        "kapha": "Slow, monotonous, sweet voice"
    },
    {
        "question": "How do you walk?",
        "vata": "Fast, light steps",
        "pitta": "Moderate, purposeful",
        "kapha": "Slow, steady, graceful"
    },
    {
        "question": "How do you spend money?",
        "vata": "Impulsive, spend on trifles",
        "pitta": "Planned, spend on luxury items",
        "kapha": "Save money, reluctant to spend"
    },
    {
        "question": "What is your energy level throughout the day?",
        "vata": "Comes in bursts, tire easily",
        "pitta": "Steady, high energy",
        "kapha": "Steady but slow to start"
    },
    {
        "question": "How is your stamina/endurance?",
        "vata": "Poor, low endurance",
        "pitta": "Moderate endurance",
        "kapha": "Excellent endurance"
    },
]


def prakriti_test(request):
    return render(request, "patient-portal/predict.html", {
        "questions": PRAKRITI_QUESTIONS
    })



def prakriti_submit(request):
    if request.method != "POST":
        return redirect("prakriti_test")

    total = len(PRAKRITI_QUESTIONS)
    vata = pitta = kapha = 0

    for i in range(1, total+1):
        ans = request.POST.get(f"q{i}")
        if ans == "vata":
            vata += 1
        elif ans == "pitta":
            pitta += 1
        elif ans == "kapha":
            kapha += 1

    request.session["prakriti_result"] = {
        "vata": vata,
        "pitta": pitta,
        "kapha": kapha,
        "total": total
    }

    return redirect("prakriti_result")


def prakriti_result(request):
    result = request.session.get("prakriti_result")

    if not result:
        return redirect("prakriti_test")

    vata = round((result["vata"] / result["total"]) * 100)
    pitta = round((result["pitta"] / result["total"]) * 100)
    kapha = round((result["kapha"] / result["total"]) * 100)

    dosha = max([
        ("Vata", vata),
        ("Pitta", pitta),
        ("Kapha", kapha)
    ], key=lambda x: x[1])[0]

    return render(request, "patient-portal/predict_result.html", {
        "vata": vata,
        "pitta": pitta,
        "kapha": kapha,
        "dominant": dosha
    })

   # Consent Form
# ------------------ CONSENT FORM (One-page HTML) ------------------
# Patient/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
from .models import ConsentForm
from therapist.models import Therapy

def consent_form_view(request):
    message = ""
    if request.method == "POST":
        patient_name = request.POST.get("patient_name")
        age = request.POST.get("age")
        contact = request.POST.get("contact")
        therapist_name = request.POST.get("therapist_name")
        therapy_name = request.POST.get("therapy_name")
        notes = request.POST.get("notes")
        signature = request.POST.get("signature")
        understood_risks = request.POST.get("understood_risks") == "on"
        voluntary = request.POST.get("voluntary") == "on"
        preferred_time = request.POST.get("preferred_time")

        # Get therapy description automatically
        try:
            therapy = Therapy.objects.get(name=therapy_name)
            therapy_description = therapy.description
        except Therapy.DoesNotExist:
            therapy_description = ""

        # Save to database
        consent = ConsentForm.objects.create(
            patient_name=patient_name,
            age=age,
            contact=contact,
            therapy_name=therapy_name,
            therapy_description=therapy_description,
            understood_risks=understood_risks,
            voluntary=voluntary,
            notes=notes,
            signature=signature
        )

        message = "Consent form submitted successfully!"

        # Generate PDF
        config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        context = {
    "patient_name": patient_name,
    "age": age,
    "contact": contact,
    "therapy_name": therapy_name,
    "therapist_name": therapist_name,
    "therapy_description": therapy_description,
    "notes": notes,
    "signature": signature,
    "understood_risks": "Yes" if understood_risks else "No",
    "voluntary": "Yes" if voluntary else "No",
    "preferred_time": preferred_time,
    "date": timezone.now().date(),
}

        html = render_to_string("patient-portal/consent_pdf.html", context)
        pdf = pdfkit.from_string(html, False, configuration=config)

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="consent_form.pdf"'
        return response
        return redirect('/dashboard/')

    return render(request, "patient-portal/consent_form.html", {"message": message})
