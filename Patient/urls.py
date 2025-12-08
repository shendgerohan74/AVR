from django.urls import path
from . import views
from .views import get_notifications, mark_all_notifications_read, external_notification

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
    path("api/notifications/", get_notifications, name="get_notifications"),
    path("api/notifications/read_all/", mark_all_notifications_read, name="mark_all_notifications_read"),
    path("api/external/notify/", external_notification, name="external_notification"),
]

