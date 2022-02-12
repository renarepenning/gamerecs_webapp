from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import recommender.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

# from the example coild be important
#urlpatterns = [
    #path("", recommender.views.index, name="index"),
    #path("db/", recommender.views.db, name="db"),
    #path("admin/", admin.site.urls),
#]



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

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name="front-page"), # path for home page

    path('recommender/', include('recommender.urls')), # sends urls with user prefix to user file
]

