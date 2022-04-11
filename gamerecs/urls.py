"""gamerecs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views

from accounts.views import(
    register_view,
    login_view,
    logout_view
)
from recommender.views import (
    user_view,
    get_rec,
    rate
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="front-page")  # path for home page
    # sends urls with user prefix to user file
    , path('login/', login_view, name="login")
    , path('register/', register_view, name="register")
    , path('logout/', logout_view, name="logout")
    , path('user-home/', user_view, name='user-home')
    , path('recommender/', get_rec, name="get-rec")
    , path("rate/", rate)
    , path("poster/", views.poster, name="poster")

]
