from django.db import models
from django.conf import settings
from datetime import date

# Create your models here.

User = settings.AUTH_USER_MODEL

class Entry(models.Model):
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.SET_NULL) #any user maps here
    age = models.CharField(max_length=3)
    genre = models.CharField(max_length=20)
    keyword = models.CharField(max_length=20)
    theme = models.CharField(max_length=20)
    game_modes = models.CharField(max_length=20)
    tags = models.CharField(max_length=20)
    platforms = models.CharField(max_length=20)

class Rec(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) #any user maps here
    games = models.CharField(max_length=100)
    rec = models.TextField(blank=True)
    timestamp = models.DateField(default=date.today, null=True)

#class Display(models.Model):
    #games = models.CharField(max_length=6, choices=entries, default='-----')
