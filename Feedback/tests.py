import pytest
from django.urls import reverse

from .forms import FeedbackForm
from .models import Feedback

# ADD FEEDBACK


@pytest.mark.django_db
def test_feedback_add_get(client, user):
    url = reverse("feedback-form")
    client.force_login(user)
    response = client.get(url)
    form_obj = response.context["form"]
    assert response.status_code == 200
    assert isinstance(form_obj, FeedbackForm)


@pytest.mark.django_db
def test_feedback_add_post(client, user, user_2, feedback):
    url = reverse("feedback-form")
    client.force_login(user)
    data = {
        "rating": 5,
        "opinion": "test_add_feedback",
        "pet-sit": user_2.username,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    url_redirect = reverse("petsit-view")
    assert response.url.startswith(url_redirect)
    assert Feedback.objects.get(opinion=data["opinion"])


# DELETE FEEDBACK


@pytest.mark.django_db
def test_delete_view(client, user, feedback):
    url = reverse("feedback-delete")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_post(client, user, user_2, feedback):
    url = reverse("feedback-delete")
    client.force_login(user)
    print(feedback.id)
    data = {
        "btn-delete": feedback.id,
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert Feedback.objects.filter(id=feedback.id).count() == 0
