from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages

from .forms import UserForm
from .models import User

'''from .models import xyz'''
# request handler!

# create view ==> add to urls.py here, then in parent class.


def rec_home(request):
    return render(request, 'rec_home.html')  # , context=context)

 # this is what's essentally done by the { { } } thingy in the form tag
    # if request.method == "POST":
    #     post_data = request.POST or None
    #     if post_data != None:
    #         my_form = UserForm(request.POST)
    #         if my_form.is_valid():
    #             userNameFromInput = my_form.cleaned_data.get("userName")
    #             ageFromInput = my_form.cleaned_data.get("age")
    #             genreFromInput = my_form.cleaned_data.get("genre")

    #             User.objects.create(userName=userNameFromInput,
    #                                 age=ageFromInput, genre=genreFromInput)


def add_user(request, *args, **kwargs):
    form = UserForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = UserForm()  # returned cleaned form
        # return HttpResponseRedirect("/success") # two options for redirecting after form submission
        # return redirect("/success")
    return render(request, "forms.html", {"form": form})
