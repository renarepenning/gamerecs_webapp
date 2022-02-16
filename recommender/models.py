from ast import keyword
from django.db import models

# Create your models here.

# creating dj model: resiger in settings, create in models, add in admin


class User(models.Model):
    userName = models.CharField(max_length=20)
    age = models.CharField(max_length=3)
    genre = models.CharField(max_length=10)
    keyword = models.CharField(max_length=10)
    theme = models.CharField(max_length=10)
