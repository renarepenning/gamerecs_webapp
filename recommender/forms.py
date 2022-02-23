from django import forms

from .models import Entry


class EntryForm(forms.ModelForm):
    # userName = 
    # age = forms.CharField(max_length=3)
    # genre = forms.CharField(max_length=20)
    # keyword = forms.CharField(max_length=20)
    # theme = forms.CharField(max_length=20)
    # game_modes = forms.CharField(max_length=20)
    # tags = forms.CharField(max_length=20)
    # platforms = forms.CharField(max_length=20) ## can use these to override

    class Meta:
        model = Entry
        fields = [
            'userName',
            'age',
            'genre',
            'keyword',
            'theme',
            'game_modes',
            'tags',
            'platforms'
        ]

