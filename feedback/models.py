from django.db import models
from django.contrib.auth.models import User
from therapist.models import Therapist
from therapy.models import Therapy

class Feedback(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True)
    therapy = models.ForeignKey(Therapy, on_delete=models.SET_NULL, null=True)

    rating = models.IntegerField(default=5)

    pain_change = models.CharField(max_length=20, choices=[
        ('better', 'Better'),
        ('same', 'Same'),
        ('worse', 'Worse')
    ], null=True, blank=True)

    stress_change = models.CharField(max_length=20, choices=[
        ('better', 'Better'),
        ('same', 'Same'),
        ('worse', 'Worse')
    ], null=True, blank=True)

    sleep_change = models.CharField(max_length=20, choices=[
        ('better', 'Better'),
        ('same', 'Same'),
        ('worse', 'Worse')
    ], null=True, blank=True)

    communication_rating = models.IntegerField(default=5)

    comfort_level = models.CharField(max_length=20, choices=[
        ('comfortable','Comfortable'),
        ('average','Average'),
        ('uncomfortable','Uncomfortable'),
    ], null=True, blank=True)

    feedback_text = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.patient.username}"
