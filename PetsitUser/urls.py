from django.urls import path

from .views import (
    PetForm,
    PetResultView,
    PetsitLogForm,
    PetsitLogView,
    PetStart,
    UpdateInfoView,
)

urlpatterns = [
    path("", PetStart.as_view(), name="index"),
    path("pet-form/", PetForm.as_view(), name="pet_form"),
    path("pet-result/", PetResultView.as_view(), name="result"),
    path("petsit-logview/", PetsitLogView.as_view(), name="petsit-view"),
    path("petsit-logform/", PetsitLogForm.as_view(), name="petsit-form"),
    path("petsit-update/<int:id>/", UpdateInfoView.as_view(), name="update"),
]
