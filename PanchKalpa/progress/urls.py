from django.urls import path
from . import views

urlpatterns = [
    path("", views.progress_page, name="progress-page"),
    path("api/chart/", views.progress_chart_data, name="progress-chart-data"),
]


