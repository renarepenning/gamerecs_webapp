from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
"""tutorial didn't need this but i just added it"""
from recommender.models import Entry

# Create your views here.
from .forms import LoginForm, RegisterForm

User = get_user_model()

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        try:
            user = User.objects.create_user(username, password)
        except:
            user != None
        if user != None:
            login(request, user)
            return redirect("/") 
        else:
            request.session['registration_error'] = 1
    return render(request, "forms.html", {"form": form})

## auth user into project
def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        # never want to print pword bc it will print in logs
        user = authenticate(request, username=username, password=password)
        if user != None:
            # user is valid and active -> is_active
            # request.user == user
            login(request, user)
            return redirect("/recommender/add/") 
        else:
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] += 1 # simple way to monitor attempts, but only on same session
            # return redirect("/invalid-password")
            request.session['invalid_user'] = 1
    return render(request, "loginform.html", {"form": form})

def logout_view(request):
    logout(request)
    # request.user == Anon User
    return redirect("/")