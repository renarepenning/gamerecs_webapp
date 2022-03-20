from django import forms

from .models import Entry, Rec


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            'age',
            'genre',
            'keyword',
            'theme',
            'game_modes',
            'tags',
            'platforms'
        ]


class RecForm(forms.ModelForm):
    class Meta:
        model = Rec
        fields = [
            'games'
        ]
#class DisplayForm(forms.ModelForm):
    #class Meta:
        #model = DisplayModel
        #field = ['games']

