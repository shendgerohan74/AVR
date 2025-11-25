from django.urls import path
from .views import therapist_login, therapist_dashboard, therapist_patients, session_entry, therapist_inventory, therapist_reports, therapist_teleconsult, therapist_logout

urlpatterns = [
    path("login/", therapist_login, name="therapist_login"),
    path("dashboard/", therapist_dashboard, name="therapist_dashboard"),
    path("patients/", therapist_patients, name="therapist_patients"),
    path("session-entry/", session_entry, name="session_entry"),
    path("inventory/", therapist_inventory, name="therapist_inventory"),
    path("reports/", therapist_reports, name="therapist_reports"),
    path("teleconsult/", therapist_teleconsult, name="therapist_teleconsult"),
    path("logout/", therapist_logout, name="therapist_logout"),

]
