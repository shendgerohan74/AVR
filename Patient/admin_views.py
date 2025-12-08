from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from patient.models import PatientProfile
from patient.utils import notify_patient

# Allow only admin users (superusers)
@user_passes_test(lambda u: u.is_superuser)
def admin_send_notification(request):
    patients = PatientProfile.objects.all()

    if request.method == "POST":
        patient_id = request.POST.get("patient")
        title = request.POST.get("title")
        message = request.POST.get("message")

        patient = PatientProfile.objects.get(id=patient_id)
        notify_patient(patient, title, message)

        return redirect("notification_sent_success")

    return render(request, "admin/send_notification.html", {"patients": patients})
