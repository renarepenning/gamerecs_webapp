from django.shortcuts import render
from django.http import HttpResponse

import requests
from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


#'''from .models import xyz'''
# request handler!

# create view ==> add to urls.py here, then in parent class.
def rec_home(request):

    return render(request, "db.html", {"greetings": greetings})
