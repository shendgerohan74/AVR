from django.http import HttpResponse
from Patient.utils import send_notification

def some_view(request):
    patient_id = 5  # example
    send_notification(patient_id, "Therapy Scheduled", "Your Abhyanga session is booked for tomorrow at 10 AM.")

    return HttpResponse("Notification sent")


def generate_diet_plan(prakriti, stage="none", symptoms=None):
    symptoms = symptoms or []

    FOOD_DB = {
        "Vata": {
            "good": ["Warm soup", "Ghee", "Dates"],
            "avoid": ["Dry snacks", "Cold drinks"]
        },
        "Pitta": {
            "good": ["Coconut water", "Fresh salads"],
            "avoid": ["Spicy foods", "Pickles", "Coffee"]
        },
        "Kapha": {
            "good": ["Sprouts", "Ginger tea"],
            "avoid": ["Sweets", "Dairy", "Fried food"]
        },
    }

    ROUTINE = {
        "Vata": ["Gentle yoga", "Oil massage", "Sleep before 10 PM"],
        "Pitta": ["Meditation", "Avoid heat", "Stay in cool environment"],
        "Kapha": ["Fast walk", "Cardio", "Avoid day sleep"],
    }

    STAGE_MODIFIERS = {
        "pre": "Prefer light & cleansing foods.",
        "post": "Prefer warm, soft, healing foods.",
        "during": "Eat simple, warm meals that digest easily."
    }

    base = FOOD_DB.get(prakriti, {})

    meals = {
        "breakfast": [base["good"][0]],
        "lunch": base["good"][0:2],
        "dinner": [base["good"][0]],
    }

    snacks = [base["good"][-1]]

    drinks = []
    if prakriti == "Vata":
        drinks = ["Warm ginger tea", "Cinnamon water"]
    elif prakriti == "Pitta":
        drinks = ["Coconut water", "Aloe vera juice"]
    elif prakriti == "Kapha":
        drinks = ["Ginger tea", "Warm lemon water"]

    stage_note = STAGE_MODIFIERS.get(stage, "")

    # small logic for acidity example
    if "acidity" in symptoms and prakriti == "Pitta":
        drinks.append("Fennel tea")

    return {
        "prakriti": prakriti,
        "stage": stage,
        "notes": stage_note,
        "meals": meals,
        "snacks": snacks,
        "drinks": drinks,
        "routine": ROUTINE.get(prakriti, []),
        "sleep": ["Sleep before 10 PM"] if prakriti == "Vata" else
                 ["Avoid late-night screens"] if prakriti == "Pitta" else
                 ["Wake up early; avoid day nap"]
    }
