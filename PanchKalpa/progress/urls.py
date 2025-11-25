from django.urls import path
from . import views
from .views import get_progress, save_daily_log

urlpatterns = [
    path("", views.progress_page, name="progress-page"),
    path("api/patient/progress/", get_progress, name="progress-api"),
    path("api/patient/progress/save/", save_daily_log, name="progress-save"),
    path("api/chart/", views.progress_chart_data, name="progress-chart-data"),
]

