"""
URL configuration for PanchKalpa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include
# from accounts.views import landing_page, therapist_login

# urlpatterns = [
#     path('', landing_page, name='landing'),
#     path('', include('progress.urls')),
#     path('admin/', admin.site.urls),
#     path('accounts/', include('accounts.urls')),
#     path('patient/', include('Patient.urls')),
#     path('progress/', include('progress.urls')),
#     path("billing/", include("billing.urls", namespace="billing")),
#     path("therapist/login/", therapist_login, name="therapist-login"),
#     path('therapist/', include('therapist.urls')),

# ]


from django.contrib import admin
from django.urls import path, include
from accounts.views import landing_page   # ONLY THIS

urlpatterns = [
    path('admin/', admin.site.urls),

    # Landing Page
    path('', landing_page, name="landing"),

    # Accounts App
    path('accounts/', include('accounts.urls')),

    # Therapist App
    path('therapist/', include('therapist.urls')),
    path('chat/', include('chat.urls')),

    # Patient App
    path('patient/', include('Patient.urls')),
    path("billing/", include(("billing.urls", "billing"), namespace="billing")),
    path("progress/", include("progress.urls")),

]
