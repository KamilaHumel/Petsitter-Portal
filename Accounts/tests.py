import pytest
from django.contrib.auth.models import User
from django.urls import reverse

# REGISTRATION


def test_registration(client):
    url = reverse("registration")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_registration_post(client):
    url = reverse("registration")
    data = {
        "username": "test",
        "first_name": "test",
        "last_name": "test",
        "email": "test@test.pl",
        "password1": "123",
        "password2": "123",
    }
    response = client.post(url, data)
    assert response.status_code == 302
    url_redirect = reverse("login")
    assert response.url.startswith(url_redirect)
    User.objects.get(username=data["username"])


# LOGIN


def test_login(client):
    url = reverse("login")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_post(client, user):
    url = reverse("login")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
