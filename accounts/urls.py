# from django.urls import path
# from .views import login_view, signup_view, logout_view, therapist_signup, therapist_login

# urlpatterns = [
#     path("login/", login_view, name="login"),
#     path("signup/", signup_view, name="signup"),
#     path("logout/", logout_view, name="logout"),
#     path("therapist-signup/", therapist_signup, name='doc_signup'),
#     path("therapist/login/", therapist_login, name="therapist-login"),
    

# ]
# from django.urls import path
# from .views import login_view, signup_view, logout_view, therapist_signup

# urlpatterns = [
#     path("login/", login_view, name="login"),
#     path("signup/", signup_view, name="signup"),
#     path("logout/", logout_view, name="logout"),

#     # Therapist Signup Not Allowed
#     path("therapist-signup/", therapist_signup, name="therapist-signup"),
# ]

from accounts.views import otp_login

from django.urls import path
from .views import otp_login, signup_view, logout_view, therapist_signup, landing_page, send_otp

urlpatterns = [
    path("", landing_page, name="landing"),  # THIS NOW WORKS

    path('login/', otp_login, name='login'),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path('send-otp/', send_otp, name='send-otp'),

    # Therapist Signup Not Allowed
    path("therapist-signup/", therapist_signup, name="therapist-signup"),
    
]
