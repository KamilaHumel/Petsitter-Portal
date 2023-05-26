from django.urls import path

from .views import FeedbackDeleteView, FeedbackFormView

urlpatterns = [
    path("feedback-form/", FeedbackFormView.as_view(), name="feedback-form"),
    path("feedback-delete/", FeedbackDeleteView.as_view(), name="feedback-delete"),
]
