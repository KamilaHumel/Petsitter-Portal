from django import forms

from .models import PetsitUser


class PetsitForm(forms.ModelForm):
    class Meta:
        model = PetsitUser
        fields = [
            "city",
            "address",
            "place_type",
            "transport",
            "about",
            "animals",
            "size",
        ]
        widgets = (
            {
                "about": forms.Textarea,
                "animals": forms.CheckboxSelectMultiple(),
                "size": forms.CheckboxSelectMultiple(),
            },
        )
        labels = {
            "city": "Miasto",
            "address": "Adres",
            "place_type": "Rodzaj lokalu",
            "transport": "Czy oferujesz transport",
            "about": "Kilka słów o Tobie:",
            "animals": "Jakimi zwierzętami możesz się opiekować:",
            "size": "Rozmiar zwierzaków",
        }


class PetsitSearchForm(forms.ModelForm):
    class Meta:
        model = PetsitUser
        fields = ["city", "address", "place_type", "transport", "size"]
        widgets = {"size": forms.CheckboxSelectMultiple()}
        labels = {
            "city": "Miasto",
            "address": "Adres",
            "place_type": "Rodzaj lokalu",
            "transport": "Transport",
            "size": "Rozmiar zwierzaka",
        }
