from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User



class Therapist(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    password = models.CharField(max_length=255)  # encrypted password store hoga

    def save(self, *args, **kwargs):
        # Password ko encrypt karke save karega
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Therapy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TherapistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="therapistprofile")
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
