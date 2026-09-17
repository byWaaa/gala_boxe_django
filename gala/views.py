from django.shortcuts import render

# Create your views here.

def Acceuil(request):
    return render(request, 'gala/Acceuil.html')