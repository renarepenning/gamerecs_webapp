from django.db import models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Entry(models.Model):
    userName = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    age = models.CharField(max_length=3)
    genre = models.CharField(max_length=20)
    keyword = models.CharField(max_length=20)
    theme = models.CharField(max_length=20)
    game_modes = models.CharField(max_length=20)
    tags = models.CharField(max_length=20)
    platforms = models.CharField(max_length=20)
