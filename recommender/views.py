from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib import messages

'''from .models import myUser, Game, Mood'''
# request handler!

# create view ==> add to urls.py here, then in parent class.
def rec_home(request):
    #return HttpResponse('Welcome to our capstone website \n user page')
    '''context = {
        'num_users': myUser.objects.all().count(),
        'num_games': Game.objects.all().count(),
    }'''


    return render(request, 'rec_home.html')# , context=context)