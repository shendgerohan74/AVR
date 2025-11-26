from django.urls import path
from .views import login_view, signup_view, logout_view, therapist_signup, therapist_login

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("therapist-signup/", therapist_signup, name='doc_signup'),
    path("therapist/login/", therapist_login, name="therapist-login"),
    

]
