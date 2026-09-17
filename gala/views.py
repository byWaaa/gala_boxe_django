from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from gala.form import InscriptionForm

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