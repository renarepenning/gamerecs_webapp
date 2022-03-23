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
    form = EntryForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = EntryForm()  # returned cleaned form
        return redirect("/user-home")
    return render(request, "entryform.html", {"title":"tester form", "form": form})

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

def rate(request):
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        # print("el_id", el_id)
        val = request.POST.get('val')
        # print("VALUE", val)
        obj = Rec.objects.get(id=el_id)
        obj.score = val
        obj.save()
        print("obj", obj, "  score ", obj.score)
        return JsonResponse({'success':'true', 'score': val}, safe=False)
    return JsonResponse({'success':'false'})