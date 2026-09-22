from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login
from django.shortcuts import redirect
from gala.forms import InscriptionForm
from gala.models import Gala, Boxeur
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ClubForm, BoxeurForm
from .models import Club
from django.db.models import ProtectedError
# Create your views here.

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
    boxeur = get_object_or_404(boxeur, boxeur_id)
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