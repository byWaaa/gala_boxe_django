from django.contrib import admin
from .models import Club, CategoriePoids, Boxeur, Gala, Arbitre, Combat, Billet, HistoriqueSuppression
# Register your models here.

admin.site.register(CategoriePoids)
admin.site.register(Arbitre)
admin.site.register(HistoriqueSuppression)
admin.site.register(Billet)

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'nombre_combattants')
    list_filter = ('ville',)
    serach_fields = ('nom', 'ville')

@admin.register(Boxeur)
class BoxeurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'club', 'categorie', 'statut')
    list_filter = ('club', 'categorie', 'statut')
    search_fields = ('nom', 'prenom')


@admin.register(Gala)
class GalaAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date', 'ville', 'statut')
    list_filter = ('statut',)
    search_fields = ('nom', 'ville')


@admin.register(Combat)
class CombatAdmin(admin.ModelAdmin):
    list_display = ('gala', 'boxeur_rouge', 'boxeur_bleu', 'type_combat', 'resultat')
    list_filter = ('gala', 'type_combat', 'resultat')
