from django.contrib import admin

# Register your models here.
from .models import Entry, Rec
admin.site.register(Entry)
admin.site.register(Rec)
