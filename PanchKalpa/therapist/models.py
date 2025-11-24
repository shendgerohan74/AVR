from django.db import models
from django.contrib.auth.hashers import make_password

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
