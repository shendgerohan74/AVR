from django.urls import path
from . import views

urlpatterns = [
    path("send/", views.send_message),
    path("get/<int:therapist_id>/", views.get_messages),
]
