from django import forms
from Feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'opinion']
        widgets = {'opinion': forms.Textarea,
                   }