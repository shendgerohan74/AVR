from django.urls import path
from .views import therapist_login, therapist_dashboard, therapist_logout

urlpatterns = [
    path('login/', therapist_login, name='therapist-login'),
    path('dashboard/', therapist_dashboard, name='therapist-dashboard'),
    path('logout/', therapist_logout, name='therapist-logout'),
]
