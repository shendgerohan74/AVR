from django.urls import path
from .views import progress_page, get_progress, save_daily_log

urlpatterns = [
    # Page View
    path("", progress_page, name="progress-page"),

    # API Endpoints (THE ONLY ONES USED BY FRONTEND)
    path("api/patient/progress/", get_progress, name="progress-api"),
    path("api/patient/progress/save/", save_daily_log, name="progress-save"),
]

# from django.urls import path
# from . import views
# from .views import get_progress, save_daily_log

# urlpatterns = [
#     path("", views.progress_page, name="progress-page"),

#     # ⭐ THIS IS THE REQUIRED URL FOR DASHBOARD CHART
#     # path("chart-data/", views.progress_chart_data, name="progress-chart-data"),
#     path("api/chart/", views.progress_chart_data, name="progress-chart-data"),

#     # Other APIs (keep them)
#     path("api/patient/progress/", views.get_progress, name="progress-api"),
#     path("api/patient/progress/save/", views.save_daily_log, name="progress-save_log"),

#     # Duplicates (safe)
#     path("get-progress/", views.get_progress, name="get_progress"),
#     path("progress-data/", views.progress_chart_data, name="progress_chart_data"),
#     path("save-daily/", views.save_daily_log, name="save_daily_log"),
# ]
