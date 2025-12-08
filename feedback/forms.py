from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'therapy',
            'therapist',
            'rating',
            'pain_change',
            'stress_change',
            'sleep_change',
            'communication_rating',
            'comfort_level',
            'feedback_text'
        ]

        widgets = {
            'therapy': forms.Select(attrs={'class': 'feedback-field'}),
            'therapist': forms.Select(attrs={'class': 'feedback-field'}),
            
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'feedback-field'
            }),
            
            'pain_change': forms.Select(attrs={'class': 'feedback-field'}),
            'stress_change': forms.Select(attrs={'class': 'feedback-field'}),
            'sleep_change': forms.Select(attrs={'class': 'feedback-field'}),
            
            'communication_rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'feedback-field'
            }),
            
            'comfort_level': forms.Select(attrs={'class': 'feedback-field'}),
            
            'feedback_text': forms.Textarea(attrs={
                'rows': 4,
                'class': 'feedback-field feedback-textarea'
            }),
        }
