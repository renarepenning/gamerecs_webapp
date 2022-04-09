from sqlite3 import Timestamp
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib import messages
from django.template import RequestContext

from .forms import EntryForm, RecForm
from .models import Entry, Rec

"""TEST INPUT FILE W FUNCTION"""
from .algorithm.code import getRec


from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()                         

@login_required
def add_entry(request, *args, **kwargs):
    userid = request.user.pk # gives primary key
    entry = Entry.objects.all().filter(user_id=userid)

    form = EntryForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = EntryForm()  # returned cleaned form
        return redirect("/user-home")
    return render(request, "entryform.html", {"prof":entry, "form": form})

@login_required
def user_view(request):
    # https://www.youtube.com/watch?v=VxOsCKMStuw
    userid = request.user.pk # gives primary key
    entries = Entry.objects.all().filter(user_id=userid)
    inputs = Rec.objects.all().filter(user_id=userid).order_by('timestamp')[:10:-1]
    args = {'user': request.user, 'entries': entries, 'recs': inputs}
    return render(request, "user.html", args)

@login_required
def get_rec(request, *args, **kwargs):
    form = RecForm(request.POST or None)
    obj = None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        ## CALL FUNCTION ON THE GAME THAT WAS INPUT
        obj.rec = getRec(obj.games)
        ##
        obj.save()
        form = RecForm()  # returned cleaned form
        #return redirect("/user-home")
    return render(request, "recform.html", {"form": form, "obj":obj})# "rec": obj.rec, "obj":obj})

# @transaction.commit_manually
def rate(request):
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        obj = Rec.objects.get(id=el_id)
        obj.rating = int(val)
        obj.save()

        # https://stackoverflow.com/questions/50782502/django-save-method-not-saving
        return JsonResponse({'success':'true', 'rating': obj.rating}, safe=False)
    return JsonResponse({'success':'false'})
    """ select * from recommender_rec where recommender_rec.id=85; """

