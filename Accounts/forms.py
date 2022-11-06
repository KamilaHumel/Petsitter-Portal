from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(max_length=128)
    password2 = forms.CharField(max_length=128)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        data = super().clean()
        password1 = data['password1']
        password2 = data['password2']
        if password1 != password2:
            raise ValidationError("Hasła muszą być takie same w obydwu polach!")
        return data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


