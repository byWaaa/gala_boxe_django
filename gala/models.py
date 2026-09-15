from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Club(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    ville = models.CharField(max_length=100)
    date_fondation = models.DateField()
    nombre_combattants = models.PositiveIntegerField(default=0)
    logo = models.ImageField(upload_to='clubs/', blank=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']


class CategoriePoids(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    poids_min = models.DecimalField(max_digits=5, decimal_places=2)
    poids_max = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['poids_min']
        verbose_name_plural = "Catégories de poids"


class Boxeur(models.Model):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('retraite', 'Retraité'),
        ('suspendu', 'Suspendu'),
    ]
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    nationalite = models.CharField(max_length=100)
    taille_cm = models.PositiveIntegerField()
    envergure_cm = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='boxeurs/', blank=True, null=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='boxeurs')
    categorie = models.ForeignKey(CategoriePoids, on_delete=models.PROTECT, related_name='boxeurs')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        ordering = ['nom', 'prenom']


class Gala(models.Model):
    STATUT_CHOICES = [
        ('a_venir', 'À venir'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]

    nom = models.CharField(max_length=100)
    date = models.DateField()
    lieu = models.CharField(max_length=150)
    ville = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    affiche = models.ImageField(upload_to='galas/', blank=True, null=True)
    organisateur = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='galas_organises')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_venir')
    capacite_max = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nom} - {self.date} - {self.lieu}, {self.ville}"

    class Meta:
        ordering = ['date', 'nom']

class Arbitre(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        ordering = ['nom', 'prenom']
        
class Combat(models.Model):
    RESULTAT_CHOICES = [
        ('non_joue', 'Pas encore joué'),
        ('victoire_rouge', 'Victoire coin rouge'),
        ('victoire_bleu', 'Victoire coin bleu'),
        ('nul', 'Match nul'),
    ]
    METHODE_CHOICES = [
        ('ko', 'KO'),
        ('tko', 'TKO / Arrêt de l\'arbitre'),
        ('decision', 'Décision'),
        ('abandon', 'Abandon'),
        ('disqualification', 'Disqualification'),
    ]
    TYPE_COMBAT_CHOICES = [
        ('preliminaire', 'Préliminaire'),
        ('co_main', 'Co-main event'),
        ('main_event', 'Main event'),
    ]

    gala = models.ForeignKey(Gala, on_delete=models.CASCADE, related_name='combats')
    boxeur_rouge = models.ForeignKey(Boxeur, on_delete=models.PROTECT, related_name='combats_rouge')
    boxeur_bleu = models.ForeignKey(Boxeur, on_delete=models.PROTECT, related_name='combats_bleu')
    categorie = models.ForeignKey(CategoriePoids, on_delete=models.PROTECT)
    arbitre_principal = models.ForeignKey(Arbitre, on_delete=models.SET_NULL, null=True, related_name='combats_principal')
    arbitre_assistant = models.ForeignKey(Arbitre, on_delete=models.SET_NULL, null=True, blank=True, related_name='combats_assistant')
    type_combat = models.CharField(max_length=20, choices=TYPE_COMBAT_CHOICES, default='preliminaire')
    nb_rounds = models.PositiveIntegerField()  # dépend du type_combat, voir validation
    resultat = models.CharField(max_length=20, choices=RESULTAT_CHOICES, default='non_joue')
    methode = models.CharField(max_length=20, choices=METHODE_CHOICES, blank=True, null=True)
    ordre = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.boxeur_rouge} vs {self.boxeur_bleu} - {self.gala.nom}"

    class Meta:
        ordering = ['gala', 'ordre']


class HistoriqueSuppression(models.Model):
    description_combat = models.CharField(max_length=255)  # ex: "Dupont vs Martin - Gala X"
    raison = models.TextField()
    supprime_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_suppression = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suppression: {self.description_combat} par {self.supprime_par} le {self.date_suppression}"

    class Meta:
        ordering = ['-date_suppression']
        verbose_name_plural = "Historiques de suppression"

class Billet(models.Model):
    TYPE_PLACE_CHOICES = [
        ('gradin', 'Gradin'),
        ('ringside', 'Ringside'),
        ('vip', 'VIP'),
    ]
    gala = models.ForeignKey(Gala, on_delete=models.CASCADE, related_name='billets')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billets')
    type_place = models.CharField(max_length=20, choices=TYPE_PLACE_CHOICES)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    date_achat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billet {self.type_place} pour {self.gala.nom} acheté par {self.utilisateur.username}"

    class Meta:
        ordering = ['-date_achat']