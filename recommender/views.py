from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib import messages

'''from .models import xyz'''
# request handler!

# create view ==> add to urls.py here, then in parent class.
def rec_home(request):

    return render(request, 'rec_home.html')# , context=context)