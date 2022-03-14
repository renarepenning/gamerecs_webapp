from cProfile import label
from django.contrib.auth import get_user_model
from django import forms
# check for unique email and username

User = get_user_model() #import user model

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    """THESE DO NOT YET CHECK FOR MATCHS. PWORD WILL BE FIRST ONE"""
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password"
            }
        )
    )

    def clean_username(self): # makes sure username is correct
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please pick another.")
        return username

    """def clean_email(self): """
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
        attrs={
        "class": "form-control"
    })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )

    """def clean(self): # could have addtl form val
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")"""


    def clean_username(self): # makes sure username is correct
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user")
        if qs.count() != 1:
            raise forms.ValidationError("This is an invalid user.")
        return username