from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login
from django.shortcuts import redirect
from gala.forms import InscriptionForm
from gala.models import Gala, Boxeur
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .forms import ClubForm, BoxeurForm, GalaForm, CombatForm, RaisonSuppressionForm, AchatBilletForm
from .models import Club, Gala, Combat, HistoriqueSuppression, Billet
from django.db.models import ProtectedError
# Create your views here.

PRIX_PLACES = {
    'gradin': 35.00,
    'ringside': 85.00,
    'vip': 120.00,
}

def accueil(request):
    return render(request, 'gala/accueil.html')

def inscription(request):
    if(request.method == 'POST'):
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès. Bienvenue dans TheMainEvent !")
            return redirect('gala:accueil')
    else :
        form = InscriptionForm()
    return render(request, 'gala/inscription.html', {'form': form})

def liste_galas(request):
    galas_list = Gala.objects.all()
    paginator = Paginator(galas_list, 6)  # Show 10 galas per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'gala/gala_liste.html', {'page_obj': page_obj})

def detail_gala(request, gala_id):
    gala = get_object_or_404(Gala, id=gala_id)
    combat = gala.combats.all()  
    return render(request, 'gala/gala_detail.html', {'gala': gala, 'combats': combat})

def liste_boxeur(request):
    boxeur_list = Boxeur.objects.all()
    paginator = Paginator(boxeur_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'gala/boxeur_liste.html', {'page_obj': page_obj})

def detail_boxeur(request, boxeur_id):
    boxeur = get_object_or_404(Boxeur, id=boxeur_id)
    combats = boxeur.combats_rouge.all() | boxeur.combats_bleu.all()
    return render(request, 'gala/boxeur_detail.html', {'boxeur': boxeur, 'combats': combats})

#CRUD FORMULAIRE
@staff_member_required
def liste_clubs(request):
    clubs = Club.objects.all()
    return render(request, 'gala/club_liste.html', {'clubs':clubs})

@staff_member_required
def ajouter_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            messages.success(request, "Club ajouté avec succès.")
            return redirect('gala:liste_clubs')
    else :
        form = ClubForm()
    return render(request, 'gala/club_form.html', {'form': form})

@staff_member_required
def modifier_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, "Club modifié avec succès.")
            return redirect('gala:liste_clubs')
    else:
        form = ClubForm(instance=club)
    return render(request, 'gala/club_form.html', {'form': form})

@staff_member_required
def supprimer_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.method == 'POST':
        club.delete()
        messages.success(request, "Club supprimé avec succès.")
        return redirect('gala:liste_clubs')
    return render(request, 'gala/club_confirmer_suppression.html', {'club': club})

@staff_member_required
def liste_boxeurs_staff(request):
    boxeurs = Boxeur.objects.all()
    return render(request, 'gala/boxeur_liste_staff.html', {'boxeurs':boxeurs})

@staff_member_required
def ajouter_boxeur(request):
    if request.method == 'POST':
        form = BoxeurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Boxeur ajouté avec succès.")
            return redirect('gala:liste_boxeurs_staff')
    else:
        form = BoxeurForm()
    return render(request, 'gala/boxeur_form.html', {'form':form})

@staff_member_required
def modifier_boxeur(request, boxeur_id):
    boxeur = get_object_or_404(Boxeur, id=boxeur_id)
    if request.method == 'POST':
        form = BoxeurForm(request.POST, request.FILES, instance=boxeur)
        if form.is_valid():
            form.save()
            messages.success(request,"Boxeur modifié avec succès.")
    else:
        form = BoxeurForm(instance=boxeur)
    return render(request, 'gala/boxeur_form.html', {'form': form})

@staff_member_required
def supprimer_boxeur(request, boxeur_id):
    boxeur = get_object_or_404(boxeur, boxeur_id)
    if request.method == 'POST':
        try:
            boxeur.delete()
            messages.success("Boxeur supprimé avec succès.")
        except ProtectedError:
            messages.error("Impossible de supprimer ce boxeur. Il a deja un combat en cours")
        return redirect('gala:liste_boxeurs_staff')
    return render(request, 'gala/boxeur_confirmer_suppression.html', {'boxeur': boxeur})

@staff_member_required
def liste_galas_staff(request):
    galas = Gala.objects.all()
    return render(request, 'gala/gala_liste_staff.html', {'galas': galas})

@staff_member_required
def ajouter_gala(request):
    if request.method == 'POST':
        form = GalaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Gala ajouté avec succès.")
            return redirect('gala:liste_galas_staff')
    else:
        form = GalaForm()
    return render(request, 'gala/gala_form.html', {'form': form})

@staff_member_required
def modifier_gala(request, gala_id):
    gala = get_object_or_404(Gala, id=gala_id)
    if request.method == 'POST':
        form = GalaForm(request.POST, request.FILES, instance=gala)
        if form.is_valid():
            form.save()
            messages.success(request, "Gala modifié avec succès.")
            return redirect('gala:liste_galas_staff')
    else:
        form = GalaForm(instance=gala)
    return render(request, 'gala/gala_form.html', {'form': form})

@staff_member_required
def supprimer_gala(request, gala_id):
    gala = get_object_or_404(Gala, id=gala_id)
    if request.method == 'POST':
        gala.delete()
        messages.success(request, "Gala supprimé avec succès.")
        return redirect('gala:liste_galas_staff')
    return render(request, 'gala/gala_confirmer_suppression.html', {'gala': gala})

@staff_member_required
def liste_combats_staff(request):
    combats = Combat.objects.all()
    return render(request, 'gala/combat_liste_staff.html', {'combats': combats})

@staff_member_required
def ajouter_combat(request):
    if request.method == 'POST':
        form = CombatForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Combat ajouté avec succès.")
            return redirect('gala:liste_combats_staff')
    else:
        form = CombatForm()
    return render(request, 'gala/combat_form.html', {'form': form})

@staff_member_required
def modifier_combat(request, combat_id):
    combat = get_object_or_404(Combat, id=combat_id)
    if request.method == 'POST':
        form = CombatForm(request.POST, instance=combat)
        if form.is_valid():
            form.save()
            messages.success(request, "Combat modifié avec succès.")
            return redirect('gala:liste_combats_staff')
    else:
        form = CombatForm(instance=combat)
    return render(request, 'gala/combat_form.html', {'form': form})

@staff_member_required
def supprimer_combat(request, combat_id):
    combat = get_object_or_404(Combat, id=combat_id)
    if request.method == 'POST':
        form = RaisonSuppressionForm(request.POST)
        if form.is_valid():
            HistoriqueSuppression.objects.create(
                description_combat=str(combat),
                raison=form.cleaned_data['raison'],
                supprime_par=request.user
            )
            combat.delete()
            messages.success(request, "Combat supprimé avec succès. La raison a été archivée.")
            return redirect('gala:liste_combats_staff')
    else:
        form = RaisonSuppressionForm()
    return render(request, 'gala/combat_confirmer_suppression.html', {'combat': combat, 'form': form})

@login_required
def acheter_billet(request, gala_id):
    gala = get_object_or_404(Gala, id=gala_id)
    places_vendues = gala.billets.count()
    places_restantes = gala.capacite_max - places_vendues

    if request.method == 'POST':
        form = AchatBilletForm(request.POST)
        if form.is_valid():
            if places_restantes <= 0:
                messages.error(request, "Ce gala est complet, plus aucune place disponible.")
                return redirect('gala:detail_gala', gala_id=gala.id)

            type_place = form.cleaned_data['type_place']
            prix = PRIX_PLACES[type_place]  # prix déterminé ici, pas depuis le formulaire

            Billet.objects.create(
                gala=gala,
                utilisateur=request.user,
                type_place=type_place,
                prix=prix
            )
            messages.success(request, f"Billet {type_place} acheté avec succès pour {prix}$.")
            return redirect('gala:mes_billets')
    else:
        form = AchatBilletForm()

    return render(request, 'gala/acheter_billet.html', {
        'gala': gala,
        'form': form,
        'places_restantes': places_restantes,
        'prix_places': PRIX_PLACES,
    })

@login_required
def mes_billets(request):
    billets = Billet.objects.filter(utilisateur=request.user)
    return render(request, 'gala/mes_billets.html', {'billets': billets})

def accueil(request):
    prochains_galas = Gala.objects.filter(statut='a_venir').order_by('date')[:3]
    dernier_gala_termine = Gala.objects.filter(statut='termine').order_by('-date').first()

    nb_boxeurs_actifs = Boxeur.objects.filter(statut='actif').count()
    nb_galas = Gala.objects.count()
    nb_combats = Combat.objects.count()

    # Le boxeur avec le plus de victoires (calculé sur tous les boxeurs, en Python)
    tous_boxeurs = Boxeur.objects.all()
    meilleur_boxeur = max(tous_boxeurs, key=lambda b: b.victoires, default=None)

    return render(request, 'gala/accueil.html', {
        'prochains_galas': prochains_galas,
        'dernier_gala_termine': dernier_gala_termine,
        'nb_boxeurs_actifs': nb_boxeurs_actifs,
        'nb_galas': nb_galas,
        'nb_combats': nb_combats,
        'meilleur_boxeur': meilleur_boxeur,
    })