from .models import Notification, PatientProfile

def send_notification(patient_id, title, message):
    try:
        patient = PatientProfile.objects.get(id=patient_id)
        Notification.objects.create(
            patient=patient,
            title=title,
            message=message,
        )
        return True
    except PatientProfile.DoesNotExist:
        return False

def notify_patient(patient, title, message):
    Notification.objects.create(
        patient=patient,
        title=title,
        message=message
    )