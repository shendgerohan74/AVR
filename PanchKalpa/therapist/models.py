from django.db import models
from django.contrib.auth.hashers import make_password


# =============== CENTER ==================
class Center(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.city})"


# =============== THERAPY ==================
class Therapy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# =============== THERAPIST ==================
class Therapist(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    password = models.CharField(max_length=255)

    center = models.ForeignKey(Center, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    experience = models.IntegerField(default=1)

    # Expertise → Free Text (typing only)
    expertise = models.TextField(
        blank=True,
        help_text="Enter expertise separated by commas"
    )

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =============== AVAILABLE SLOT ==================
class AvailableSlot(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.therapist.name} → {self.start_time} - {self.end_time}"




class Appointment(models.Model):
    therapist = models.ForeignKey(
        Therapist,
        on_delete=models.CASCADE,
        related_name="therapist_appointments"   # FIXED
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    patient_name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.therapist.name} - {self.date} ({self.start_time} to {self.end_time})"
