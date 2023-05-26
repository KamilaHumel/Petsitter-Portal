import pytest
from django.urls import reverse

from .forms import ServicesForm
from .models import Services

# TEST - KONFIGURACJA ŚRODOWISKA


@pytest.mark.django_db
def test_check_settings():
    assert True


# ADD SERVICES


@pytest.mark.django_db
def test_services_add_get(client, user):
    url = reverse("services-form")
    client.force_login(user)
    response = client.get(url)
    form_obj = response.context["form"]
    assert response.status_code == 200
    assert isinstance(form_obj, ServicesForm)


@pytest.mark.django_db
def test_services_add_post(client, user, user_2, animals, animal_size):
    url = reverse("services-form")
    client.force_login(user)
    data = {
        "date_start": "2022-11-1",
        "date_end": "2022-11-10",
        "message": "test",
        "pet-sit": user_2.username,
        "pet-type": "KOT",
        "pet-size": animal_size[0].id,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Services.objects.get(message=data["message"])


# SERVICES VIEW


@pytest.mark.django_db
def test_services_all_view_get(client, user, services):
    url = reverse("services-all")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["results_ordered"].count() == 1


@pytest.mark.django_db
def test_services_all_accept_post(client, user, services):
    url = reverse("services-all")
    client.force_login(user)
    data = {
        "btn-appr": services.id,
    }
    response = client.post(url, data)
    assert response.status_code == 200
    s = Services.objects.get(id=data["btn-appr"])
    assert s.is_approved == True
