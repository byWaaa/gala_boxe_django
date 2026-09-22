from django.urls import path
from . import views

app_name = 'gala'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
    path('galas/', views.liste_galas, name='liste_galas'),
    path('galas/<int:gala_id>/', views.detail_gala, name='detail_gala'),
    path('boxeurs/', views.liste_boxeur, name='liste_boxeurs'),
    path('boxeurs/<int:boxeur_id>/', views.detail_boxeur, name='detail_boxeur'),
]

