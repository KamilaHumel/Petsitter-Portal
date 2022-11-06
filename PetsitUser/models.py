from django.contrib.auth.models import User
from django.db import models


PLACE_TYPE = (
    (0, 'MIESZKANIE'),
    (1, 'DOM'),
)

ANIMAL_SIZE = (
    (0, 'BARDZO MAŁY - do 2 kg'),
    (1, 'MAŁY - 2-5 kg'),
    (2, 'ŚREDNI - 5-12 kg'),
    (3, 'DUŻY - 12-20 kg'),
    (4, 'BARDZO DUŻY - powyżej 20 kg'),
)


class Animal(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


class AnimalSize(models.Model):
    size = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.size}"


class PetsitUser(models.Model):
    city = models.CharField(max_length=120, default='Warszawa')
    address = models.CharField(max_length=164)
    place_type = models.IntegerField(choices=PLACE_TYPE, default=0)
    transport = models.BooleanField(default=False)
    about = models.TextField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    animals = models.ManyToManyField(Animal)
    size = models.ManyToManyField(AnimalSize)
