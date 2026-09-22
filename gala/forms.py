from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Club

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")



class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['nom', 'ville', 'date_fondation', 'nombre_combattants', 'logo']
        widgets = {
            'date_fondation': forms.DateInput(attrs={'type': 'date'}),
        }