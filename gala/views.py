from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login
from django.shortcuts import redirect
from gala.form import InscriptionForm
from gala.models import Gala
from django.core.paginator import Paginator
# Create your views here.

def acceuil(request):
    return render(request, 'gala/Acceuil.html')

def inscription(request):
    if(request.method == 'POST'):
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès. Bienvenue dans TheMainEvent !")
            return redirect('gala:acceuil')
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