from ast import keyword
from django.db import models

# Create your models here.


class User(models.Model):
    userName = models.CharField(max_length=20)
    age = models.CharField(max_length=3)
    genre = models.CharField(max_length=10)
    keyword = models.CharField(max_length=10)
