from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.therapist_login, name="therapist_login"),

    path("dashboard/", views.therapist_dashboard, name="therapist_dashboard"),
    path("patients/", views.therapist_patients, name="therapist_patients"),
    path("session-entry/", views.session_entry, name="session_entry"),
    path("inventory/", views.therapist_inventory, name="therapist_inventory"),
    path("reports/", views.therapist_reports, name="therapist_reports"),
    path("teleconsult/", views.therapist_teleconsult, name="therapist_teleconsult"),
]
