from django.db import models

# Create your models here.


class User(models.Model):
    userName = models.CharField(max_length=20)
    age = models.CharField(max_length=3)
    genre = models.CharField(max_length=20)
    keyword = models.CharField(max_length=20)
    theme = models.CharField(max_length=20)
    game_modes = models.CharField(max_length=20)
    tags = models.CharField(max_length=20)
    platforms = models.CharField(max_length=20)
