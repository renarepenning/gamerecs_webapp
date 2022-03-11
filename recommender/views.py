from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages

from .forms import EntryForm, RecForm
from .models import Entry, Rec

"""TEST INPUT FILE W FUNCTION"""
from .algorithm.code import getRec


from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()                         

@login_required
def add_entry(request, *args, **kwargs):
    form = EntryForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = EntryForm()  # returned cleaned form
        return redirect("/user-home")
    return render(request, "forms.html", {"title":"tester form", "form": form, "rec":""})

@login_required
def user_view(request):
    # https://www.youtube.com/watch?v=VxOsCKMStuw
    userid = request.user.pk # gives primary key
    entries = Entry.objects.all().filter(user_id=userid)
    inputs = Rec.objects.all().filter(user_id=userid)
    args = {'user': request.user, 'entries': entries, 'recs': inputs}
    return render(request, "user.html", args)

@login_required
def get_rec(request, *args, **kwargs):
    form = RecForm(request.POST or None)
    rec = ""
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        ## CALL FUNCTION ON THE GAME THAT WAS INPUT
        obj.rec = getRec(obj.games)
        rec = obj.rec
        ##
        obj.save()
        form = RecForm()  # returned cleaned form
        #return redirect("/user-home")
    return render(request, "forms.html", {"title":"Get a recommendation", "form": form, "rec": rec})


