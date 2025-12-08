from django.urls import path
from . import views
from django.urls import path
from django.urls import path
from .views import consent_form_view


urlpatterns = [
    path('dashboard/', views.dashboard, name='patient-dashboard'),
    path('appointments/', views.appointments, name='patient-appointments'),
    # path('billing/', views.billing, name='patient-billing'),
    path('profile/', views.profile, name='patient-profile'),
    path("update-profile/", views.update_profile, name="update-profile"),
    path("appointments/", views.appointments, name="patient-appointments"),
    path('progress/', views.progress, name='patient-progress'),
    path('teleconsult/', views.teleconsult, name='patient-teleconsult'),
    path("api/diet/plan/", views.diet_plan_api, name="diet_plan_api"),
    path("predict/", views.prakriti_test, name="prakriti_test"),
    path("predict/submit/", views.prakriti_submit, name="prakriti_submit"),
    path("predict/result/", views.prakriti_result, name="prakriti_result"),
    

    path("dashboard/", views.dashboard, name="patient-dashboard"),
    path('consent/', consent_form_view, name='consent_form')

]

     







