from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[
        ("patient", "Patient"),
        ("therapist", "Therapist"),
        ("admin", "Admin"),
    ])
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        from datetime import timedelta, datetime
        return self.created_at < datetime.now(self.created_at.tzinfo) - timedelta(minutes=5)
