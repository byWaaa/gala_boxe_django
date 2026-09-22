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
    path('clubs/', views.liste_clubs, name='liste_clubs'),
    path('clubs/ajouter/', views.ajouter_club, name='ajouter_club'),
    path('clubs/<int:club_id>/modifier/', views.modifier_club, name='modifier_club'),
    path('clubs/<int:club_id>/supprimer/', views.supprimer_club, name='supprimer_club'),
]

