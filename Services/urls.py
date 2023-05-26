from django.urls import path

from .views import ServicesAllView, ServicesFormView

urlpatterns = [
    path("service-form/", ServicesFormView.as_view(), name="services-form"),
    path("service-all/", ServicesAllView.as_view(), name="services-all"),
]
