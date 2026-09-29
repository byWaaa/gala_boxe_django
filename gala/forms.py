from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Club, Boxeur, Gala, Combat, Billet


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

class CombatForm(forms.ModelForm):
    class Meta:
        model = Combat
        fields = ['gala', 'boxeur_rouge', 'boxeur_bleu', 'categorie',
                  'arbitre_principal', 'arbitre_assistant', 'type_combat',
                  'nb_rounds', 'ordre', 'resultat', 'methode']

    def clean(self):
        cleaned_data = super().clean()
        boxeur_rouge = cleaned_data.get('boxeur_rouge')
        boxeur_bleu = cleaned_data.get('boxeur_bleu')
        categorie = cleaned_data.get('categorie')
        type_combat = cleaned_data.get('type_combat')
        nb_rounds = cleaned_data.get('nb_rounds')

        # Règle 1 : un boxeur ne peut pas se combattre lui-même
        if boxeur_rouge and boxeur_bleu and boxeur_rouge == boxeur_bleu:
            raise forms.ValidationError("Un boxeur ne peut pas s'affronter lui-même.")

        # Règle 2 : les deux boxeurs doivent être de la même catégorie que le combat
        if boxeur_rouge and categorie and boxeur_rouge.categorie != categorie:
            raise forms.ValidationError(f"{boxeur_rouge} n'est pas dans la catégorie {categorie}.")
        if boxeur_bleu and categorie and boxeur_bleu.categorie != categorie:
            raise forms.ValidationError(f"{boxeur_bleu} n'est pas dans la catégorie {categorie}.")

        # Règle 3 : nombre de rounds cohérent avec le type de combat
        if type_combat and nb_rounds:
            bornes = {
                'preliminaire': (4, 6),
                'co_main': (6, 8),
                'main_event': (10, 12),
            }
            mini, maxi = bornes[type_combat]
            if not (mini <= nb_rounds <= maxi):
                raise forms.ValidationError(
                    f"Pour ce type de combat, le nombre de rounds doit être entre {mini} et {maxi}."
                )

        return cleaned_data

class RaisonSuppressionForm(forms.Form):
    raison = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Raison de la suppression",
        required=True
    )

class AchatBilletForm(forms.Form):
    type_place = forms.ChoiceField(choices=Billet.TYPE_PLACE_CHOICES, label="Type de place")