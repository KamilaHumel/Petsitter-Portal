import pytest
from django.urls import reverse

from .forms import PetsitForm, PetsitSearchForm
from .models import PetsitUser

# INDEX VIEW


def test_index_view(client):
    url = reverse("index")
    response = client.get(url)
    assert response.status_code == 200


# PETSITTER LOGVIEW


def test_logview_get_not_login(client):
    url = reverse("petsit-view")
    response = client.get(url)
    assert response.status_code == 302
    url_redirect = reverse("login")
    assert response.url.startswith(url_redirect)


@pytest.mark.django_db
def test_logview_get_login(client, user_2, feedback):
    url = reverse("petsit-view")
    client.force_login(user_2)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["feedback"].count() == 1


# PETSITTER LOGFORM


@pytest.mark.django_db
def test_logform_view(client, user):
    url = reverse("petsit-form")
    client.force_login(user)
    response = client.get(url)
    form_obj = response.context["form"]
    assert response.status_code == 200
    assert isinstance(form_obj, PetsitForm)


@pytest.mark.django_db
def test_logform_post(client, user_3, animals, animal_size):
    url = reverse("petsit-form")
    an = animals[0]
    an_s = animal_size[0]
    client.force_login(user_3)
    data = {
        "city": "Warszawa",
        "address": "test",
        "about": "test",
        "animals": [an.id],
        "size": [an_s.id],
        "place_type": "0",
        "transport": "True",
    }

    response = client.post(url, data)

    assert response.status_code == 302
    url_redirect = reverse("petsit-view")
    assert response.url.startswith(url_redirect)
    del data["animals"]
    del data["size"]
    PetsitUser.objects.get(**data)


# UPDATE


@pytest.mark.django_db
def test_update_view(client, user):
    url = reverse("update", args=(user.id,))
    client.force_login(user)
    data = {
        "first_name": "test",
        "last_name": "test",
        "city": "Kraków",
        "address": "test",
        "about": "test",
    }
    response = client.post(url, data)
    assert response.status_code == 302

    # test if object was updated in db:
    PetsitUser.objects.get(city=data["city"])


# SEARCH PETSITTER FORM


@pytest.mark.django_db
def test_petsitter_search_get(client, user):
    url = reverse("pet_form")
    client.force_login(user)
    response = client.get(url)
    form_obj = response.context["form"]
    assert response.status_code == 200
    assert isinstance(form_obj, PetsitSearchForm)


@pytest.mark.django_db
def test_petsitter_search_post(client, user):
    url = reverse("pet_form")
    client.force_login(user)
    data = {
        "animal": "KOT",
        "size": "1",
        "city": "Warszawa",
        "place_type": "0",
        "transport": "on",
    }
    response = client.post(url, data)
    assert response.status_code == 302
    url_redirect = reverse("result")
    assert response.url.startswith(url_redirect)


# RESULT SEARCHING PETSITTER


@pytest.mark.django_db
def test_result_view(client, user, user_2):
    session = client.session
    session["search_results"] = [user_2.petsituser.id]
    session.save()
    url = reverse("result")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
