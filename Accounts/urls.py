from django.urls import path

from .views import LoginView, Logout, RegistrationUser

urlpatterns = [
    path("registration/", RegistrationUser.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
]
