from django.urls import path
from . import views

app_name = 'gala'

urlpatterns = [
    path('', views.acceuil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
]

