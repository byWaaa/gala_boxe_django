from django.urls import path
from . import views

app_name = 'gala'

urlpatterns = [
    path('', views.Acceuil, name='Acceuil'),
]