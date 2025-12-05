from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.therapist_login, name="therapist-login"),
    path("dashboard/", views.therapist_dashboard, name="therapist-dashboard"),
    path("patients/", views.therapist_patients, name="therapist-patients"),
    path("session/", views.session_entry, name="session-entry"),
    path("inventory/", views.therapist_inventory, name="therapist-inventory"),
    path("reports/", views.therapist_reports, name="therapist-reports"),
    path("teleconsult/", views.therapist_teleconsult, name="therapist-teleconsult"),
]
