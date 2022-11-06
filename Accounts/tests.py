import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from PetsitUser.models import PetsitUser, Animal, AnimalSize
from Services.models import Services
from Feedback.models import Feedback
from Feedback.forms import FeedbackForm
from PetsitUser.forms import PetsitForm, PetsitSearchForm

# TEST - KONFIGURACJA ŚRODOWISKA
from Services.forms import ServicesForm


@pytest.mark.django_db
def test_check_settings():
    assert True

# INDEX VIEW

def test_index_view(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


# REGISTRATION

def test_registration(client):
    url = reverse('registration')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_registration_post(client):
    url = reverse('registration')
    data = {
        'username': "test",
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@test.pl',
        'password1': '123',
        'password2': '123',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    url_redirect = reverse('login')
    assert response.url.startswith(url_redirect)
    User.objects.get(username=data['username'])


# LOGIN

def test_login(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_post(client, user):
    url = reverse('login')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

# PETSITTER LOGVIEW

def test_logview_get_not_login(client):
    url = reverse('petsit-view')
    response = client.get(url)
    assert response.status_code == 302
    url_redirect = reverse('login')
    assert response.url.startswith(url_redirect)


@pytest.mark.django_db
def test_logview_get_login(client, user_2, feedback):
    url = reverse('petsit-view')
    client.force_login(user_2)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['feedback'].count() == 1


# PETSITTER LOGFORM

@pytest.mark.django_db
def test_logform_view(client, user):
    url = reverse('petsit-form')
    client.force_login(user)
    response = client.get(url)
    form_obj = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_obj, PetsitForm)


@pytest.mark.django_db
def test_logform_post(client, user_3, animals, animal_size):
    url = reverse('petsit-form')
    an = animals[0]
    an_s = animal_size[0]
    client.force_login(user_3)
    data = {
        'city': "Warszawa",
        'address': 'test',
        'about': 'test',
        'animals': [an.id],
        "size": [an_s.id],
        'place_type': '0',
        'transport': 'True',
    }

    response = client.post(url, data)

    assert response.status_code == 302
    url_redirect = reverse('petsit-view')
    assert response.url.startswith(url_redirect)
    del data['animals']
    del data['size']
    PetsitUser.objects.get(**data)


# UPDATE

@pytest.mark.django_db
def test_update_view(client, user):
    url = reverse('update', args=(user.id,))
    client.force_login(user)
    data = {
        'first_name': "test",
        'last_name': "test",
        'city': "Kraków",
        'address': 'test',
        'about': "test",
    }
    response = client.post(url, data)
    assert response.status_code == 302

    # test if object was updated in db:
    PetsitUser.objects.get(city=data['city'])


#DELETE

@pytest.mark.django_db
def test_delete_view(client, user, feedback):
    url = reverse('feedback-delete')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_post(client, user, user_2, feedback):
    url = reverse('feedback-delete')
    client.force_login(user)
    print(feedback.id)
    data = {
        'btn-delete': feedback.id,
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert Feedback.objects.filter(id=feedback.id).count() == 0


# SEARCH PETSITTER FORM

@pytest.mark.django_db
def test_petsitter_search_get(client, user):
    url = reverse('pet_form')
    client.force_login(user)
    response = client.get(url)
    form_obj = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_obj, PetsitSearchForm)


@pytest.mark.django_db
def test_petsitter_search_post(client, user):
    url = reverse('pet_form')
    client.force_login(user)
    data = {
        'animal': 'KOT',
        'size': '1',
        'city': 'Warszawa',
        'place_type': '0',
        'transport': 'on',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    url_redirect = reverse('result')
    assert response.url.startswith(url_redirect)


# RESULT SEARCHING PETSITTER

@pytest.mark.django_db
def test_result_view(client, user, user_2):
    session = client.session
    session['search_results'] = [user_2.petsituser.id]
    session.save()
    url = reverse('result')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


# ADD FEEDBACK

@pytest.mark.django_db
def test_feedback_add_get(client, user):
    url = reverse('feedback-form')
    client.force_login(user)
    response = client.get(url)
    form_obj = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_obj, FeedbackForm)


@pytest.mark.django_db
def test_feedback_add_post(client, user, user_2, feedback):
    url = reverse('feedback-form')
    client.force_login(user)
    data = {
        'rating': 5,
        'opinion': 'test_add_feedback',
        'pet-sit': user_2.username,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    url_redirect = reverse('petsit-view')
    assert response.url.startswith(url_redirect)
    assert Feedback.objects.get(opinion=data['opinion'])


# ADD SERVICES

@pytest.mark.django_db
def test_services_add_get(client, user):
    url = reverse('services-form')
    client.force_login(user)
    response = client.get(url)
    form_obj = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_obj, ServicesForm)


@pytest.mark.django_db
def test_services_add_post(client, user, user_2, animals, animal_size):
    url = reverse('services-form')
    client.force_login(user)
    data = {
        'date_start': '2022-11-1',
        'date_end': '2022-11-10',
        'message': 'test',
        'pet-sit': user_2.username,
        'pet-type': 'KOT',
        'pet-size': animal_size[0].id,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Services.objects.get(message=data['message'])


# SERVICES VIEW

@pytest.mark.django_db
def test_services_all_view_get(client, user, services):
    url = reverse('services-all')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['results_ordered'].count() == 1


@pytest.mark.django_db
def test_services_all_accept_post(client, user, services):
    url = reverse('services-all')
    client.force_login(user)
    data = {
        'btn-appr': services.id,
    }
    response = client.post(url, data)
    assert response.status_code == 200
    s = Services.objects.get(id=data['btn-appr'])
    assert s.is_approved == True
