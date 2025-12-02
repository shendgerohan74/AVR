from django.urls import path
from .views import (
    therapist_login,
    therapist_dashboard,
    therapist_patients,
    session_entry,
    therapist_inventory,
    therapist_reports,
    therapist_teleconsult,

    get_nearest_center,
    get_doctors_by_therapy,
    get_doctors_by_center,
    get_available_slots,
    book_appointment,

    save_session,           
    session_success,
    session_history      # ← correct import
)

urlpatterns = [
    path("login/", therapist_login, name="therapist-login"),
    path("dashboard/", therapist_dashboard, name="therapist-dashboard"),
    path("patients/", therapist_patients, name="therapist-patients"),
    path("session/", session_entry, name="session-entry"),
    path("inventory/", therapist_inventory, name="therapist-inventory"),
    path("reports/", therapist_reports, name="therapist-reports"),
    path("teleconsult/", therapist_teleconsult, name="therapist-teleconsult"),

    # AI APIs
    path("api/nearest-center/", get_nearest_center, name="nearest-center"),
    path("api/doctors-by-therapy/", get_doctors_by_therapy, name="doctors-by-therapy"),
    path("api/doctors-by-center/", get_doctors_by_center, name="doctors-by-center"),
    path("api/available-slots/", get_available_slots, name="available-slots"),
    path("api/book-appointment/", book_appointment, name="book-appointment"),

    # Session Note System
    path("save-session/", save_session, name="save_session"),
    path("session-success/", session_success, name="session_success"),
    path("session-history/", session_history, name="session_history"),
]
