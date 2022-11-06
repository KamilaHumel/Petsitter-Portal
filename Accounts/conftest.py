import pytest
from django.contrib.auth.models import User
from PetsitUser.models import Animal, AnimalSize, PetsitUser
from Feedback.models import Feedback
from Services.models import Services


@pytest.fixture
def animals():
    lst = []
    for x in range(5):
        lst.append(Animal(id=x, name=x))
    Animal.objects.bulk_create(lst)
    return lst


@pytest.fixture
def animal_size():
    lst = []
    for x in range(5):
        lst.append(AnimalSize.objects.create(size=x))
    return lst


@pytest.fixture
def user():
    u = User.objects.create(username='test')
    p = PetsitUser(city="Warszawa", address='test', about='test', user=u)
    p.save()
    u.refresh_from_db()
    return u


@pytest.fixture
def user_2():
    u2 = User.objects.create(username='test2')
    p2 = PetsitUser(city="Warszawa",
                    address='test',
                    about='test',
                    user=u2)
    p2.save()
    u2.refresh_from_db()
    return u2


@pytest.fixture
def user_3():
    u3 = User.objects.create(username='test3')
    u3.save()
    return u3

@pytest.fixture
def feedback(user, user_2):
    f = Feedback.objects.create(owner=user, pet_sitter=user_2, rating='3', opinion='test')
    return f


@pytest.fixture
def services(user, user_2, animals, animal_size):
    an = animals[0]
    an_s = animal_size[0]
    s = Services.objects.create(pet_sitter=user_2,
                                owner=user,
                                date_start='2022-11-10',
                                date_end='2022-11-12',
                                animal=an,
                                size=an_s,
                                message='test',
                                is_approved=False)
    return s


