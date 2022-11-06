"""Petsitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Accounts.views import RegistrationUser, LoginView, Logout
from PetsitUser.views import PetStart, PetForm, PetsitLogView, PetsitLogForm, UpdateInfoView, PetResultView
from Services.views import ServicesFormView, ServicesAllView
from Feedback.views import FeedbackFormView, FeedbackDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PetStart.as_view(), name='index'),
    path('registraion/', RegistrationUser.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name="logout"),
    path('pet-form/', PetForm.as_view(), name='pet_form'),
    path('pet-result/', PetResultView.as_view(), name='result'),
    path('petsit-logview/', PetsitLogView.as_view(), name="petsit-view"),
    path('petsit-logform/', PetsitLogForm.as_view(), name="petsit-form"),
    path('petsit-update/<int:id>/', UpdateInfoView.as_view(), name="update"),

    path('service-form/', ServicesFormView.as_view(), name="services-form"),
    path('service-all/', ServicesAllView.as_view(), name="services-all"),

    path('feedback-form/', FeedbackFormView.as_view(), name="feedback-form"),
    path('feedback-delete/', FeedbackDeleteView.as_view(), name="feedback-delete"),

]
