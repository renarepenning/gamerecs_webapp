from django.shortcuts import render
from django.http import HttpResponse

import requests
from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


<<<<<<< HEAD
'''from .models import xyz'''
# request handler!

# create view ==> add to urls.py here, then in parent class.
def rec_home(request):
=======
def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()
>>>>>>> change-name

    return render(request, "db.html", {"greetings": greetings})
