from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Club, Boxeur, Gala

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


class BoxeurForm(forms.ModelForm):

    class Meta:
        model = Boxeur
        fields = ['nom', 'prenom', 'date_naissance', 'nationalite', 'taille_cm',
                  'envergure_cm', 'photo', 'club', 'categorie', 'statut']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }


class GalaForm(forms.ModelForm):
    class Meta:
        model = Gala
        fields = ['nom', 'date', 'lieu', 'ville', 'description', 'affiche',
                  'organisateur', 'statut', 'capacite_max']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_date(self):
        from django.utils import timezone
        date = self.cleaned_data.get('date')
        if not self.instance.pk and date < timezone.now().date():
            raise forms.ValidationError("La date d'un nouveau gala ne peut pas être dans le passé.")
        return date