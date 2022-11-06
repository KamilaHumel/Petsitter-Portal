from django.contrib.auth.models import User
from django.db import models

RATING = (
    (0, "☆☆☆☆☆"),
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)


class Feedback(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_opinion")
    pet_sitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="petsit_opinion")
    opinion = models.TextField(max_length=300)
    rating = models.SmallIntegerField(choices=RATING, default=0)
