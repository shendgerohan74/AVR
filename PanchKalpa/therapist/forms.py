from django import forms
from .models import SessionNote

class SessionForm(forms.ModelForm):
    class Meta:
        model = SessionNote
        fields = [
            "patient_name",
            "therapy_performed",
            "session_notes",
            "inventory_used",
            "quantity"
        ]
