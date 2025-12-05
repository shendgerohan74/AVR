from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ChatMessage
from django.contrib.auth.models import User

@csrf_exempt
def send_message(request):
    data = json.loads(request.body)
    msg = data["message"]
    therapist_id = data["therapist_id"]
    patient = request.user

    ChatMessage.objects.create(
        patient=patient,
        therapist=User.objects.get(id=therapist_id),
        message=msg,
        sender="patient"
    )
    return JsonResponse({"status": "sent"})

def get_messages(request, therapist_id):
    patient = request.user
    messages = ChatMessage.objects.filter(patient=patient, therapist_id=therapist_id)
    
    return JsonResponse([
        {
            "sender": m.sender,
            "message": m.message,
            "time": m.timestamp.strftime("%I:%M %p")
        }
        for m in messages
    ], safe=False)
