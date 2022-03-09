from django.db import models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Entry(models.Model):
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.CASCADE) #any user maps here
    age = models.CharField(max_length=3)
    genre = models.CharField(max_length=20)
    keyword = models.CharField(max_length=20)
    theme = models.CharField(max_length=20)
    game_modes = models.CharField(max_length=20)
    tags = models.CharField(max_length=20)
    platforms = models.CharField(max_length=20)

    """def __str__(self):
        return self.userName"""
