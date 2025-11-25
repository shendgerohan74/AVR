from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='patient-dashboard'),
    path('appointments/', views.appointments, name='patient-appointments'),
    # path('billing/', views.billing, name='patient-billing'),
    path('profile/', views.profile, name='patient-profile'),
    path("update-profile/", views.update_profile, name="update-profile"),
    path("appointments/", views.appointments, name="patient-appointments"),

    path('progress/', views.progress, name='patient-progress'),
    path('teleconsult/', views.teleconsult, name='patient-teleconsult'),
]
