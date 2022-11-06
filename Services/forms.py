from django import forms
from Services.models import Services
from bootstrap_datepicker_plus.widgets import DatePickerInput


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['date_start', 'date_end', 'message']
        widgets = {'date_start': DatePickerInput(format='%Y-%m-%d'),
                   'date_end': DatePickerInput(format='%Y-%m-%d'),
                   'message': forms.Textarea}
