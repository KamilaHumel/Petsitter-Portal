from django.contrib.auth.models import User
from django.db import models
from PetsitUser.models import Animal, AnimalSize


class Services(models.Model):
    pet_sitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="services_care")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_ordered')
    date_start = models.DateField()
    date_end = models.DateField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    size = models.ForeignKey(AnimalSize, on_delete=models.CASCADE, default=1)
    message = models.TextField(max_length=500, null=True)
    is_approved = models.BooleanField(default=False)
