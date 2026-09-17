from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gala.models import Club, CategoriePoids, Boxeur, Arbitre, Gala, Combat, Billet
from datetime import date


class Command(BaseCommand):
    help = "Peuple la base de données avec un jeu de données complet"

    def handle(self, *args, **options):
        # ==========================================
        # CATÉGORIES DE POIDS (officielles)
        # ==========================================
        categories_data = [
            ("Poids mouche", 0, 50.8),
            ("Poids coq", 50.8, 53.5),
            ("Poids plume", 53.5, 57.2),
            ("Poids léger", 57.2, 61.2),
            ("Poids mi-moyen", 61.2, 66.7),
            ("Poids moyen", 66.7, 72.6),
            ("Poids mi-lourd", 72.6, 79.4),
            ("Poids lourd", 79.4, 150),
        ]
        cat = {}
        for nom, pmin, pmax in categories_data:
            obj, _ = CategoriePoids.objects.get_or_create(nom=nom, defaults={'poids_min': pmin, 'poids_max': pmax})
            cat[nom] = obj

        # ==========================================
        # CLUBS
        # ==========================================
        club1, _ = Club.objects.get_or_create(nom="Boxing Club Chicoutimi", defaults={
            'ville': "Chicoutimi", 'date_fondation': date(2010, 1, 1), 'nombre_combattants': 15
        })
        club2, _ = Club.objects.get_or_create(nom="Club Pugilistique Montréal", defaults={
            'ville': "Montréal", 'date_fondation': date(1995, 5, 20), 'nombre_combattants': 40
        })
        club3, _ = Club.objects.get_or_create(nom="Académie de Boxe Québec", defaults={
            'ville': "Québec", 'date_fondation': date(2005, 9, 10), 'nombre_combattants': 22
        })

        # ==========================================
        # ARBITRES
        # ==========================================
        arb1, _ = Arbitre.objects.get_or_create(nom="Tremblay", prenom="Marc")
        arb2, _ = Arbitre.objects.get_or_create(nom="Gagnon", prenom="Sylvie")

        # ==========================================
        # BOXEURS (18 au total, répartis dans les catégories)
        # ==========================================
        def creer_boxeur(nom, prenom, annee, nationalite, taille, envergure, club, categorie):
            b, _ = Boxeur.objects.get_or_create(nom=nom, prenom=prenom, defaults={
                'date_naissance': date(annee, 1, 1), 'nationalite': nationalite,
                'taille_cm': taille, 'envergure_cm': envergure,
                'club': club, 'categorie': categorie
            })
            return b

        # Poids mouche
        mouche_a = creer_boxeur("Bouchard", "Alex", 1999, "Canada", 165, 167, club1, cat["Poids mouche"])
        mouche_b = creer_boxeur("Lavoie", "Nick", 1998, "Canada", 163, 165, club2, cat["Poids mouche"])

        # Poids coq
        coq_a = creer_boxeur("Simard", "Jules", 1997, "Canada", 168, 170, club1, cat["Poids coq"])
        coq_b = creer_boxeur("Roy", "Éric", 2000, "Canada", 167, 169, club3, cat["Poids coq"])

        # Poids plume
        plume_a = creer_boxeur("Fortin", "Max", 1996, "Canada", 170, 172, club2, cat["Poids plume"])
        plume_b = creer_boxeur("Bélanger", "Tom", 1999, "Canada", 171, 173, club1, cat["Poids plume"])

        # Poids léger (3 boxeurs)
        leger_a = creer_boxeur("Dupont", "Alex", 1998, "Canada", 178, 180, club1, cat["Poids léger"])
        leger_b = creer_boxeur("Martin", "Sam", 1996, "Canada", 180, 182, club2, cat["Poids léger"])
        leger_c = creer_boxeur("Côté", "Léo", 1997, "Canada", 177, 179, club3, cat["Poids léger"])

        # Poids mi-moyen (3 boxeurs)
        mimoyen_a = creer_boxeur("Gauthier", "Rémi", 1995, "Canada", 175, 178, club1, cat["Poids mi-moyen"])
        mimoyen_b = creer_boxeur("Pelletier", "Vincent", 1994, "Canada", 176, 179, club2, cat["Poids mi-moyen"])
        mimoyen_c = creer_boxeur("Girard", "Hugo", 1998, "Canada", 174, 177, club3, cat["Poids mi-moyen"])

        # Poids moyen
        moyen_a = creer_boxeur("Morin", "David", 1993, "Canada", 180, 183, club1, cat["Poids moyen"])
        moyen_b = creer_boxeur("Lefebvre", "Simon", 1995, "Canada", 181, 184, club3, cat["Poids moyen"])

        # Poids mi-lourd
        milourd_a = creer_boxeur("Gagné", "Antoine", 1992, "Canada", 183, 186, club2, cat["Poids mi-lourd"])
        milourd_b = creer_boxeur("Bergeron", "Félix", 1994, "Canada", 184, 187, club1, cat["Poids mi-lourd"])

        # Poids lourd
        lourd_a = creer_boxeur("Boivin", "Marc-André", 1990, "Canada", 190, 193, club3, cat["Poids lourd"])
        lourd_b = creer_boxeur("Beaulieu", "Olivier", 1991, "Canada", 191, 194, club2, cat["Poids lourd"])

        # ==========================================
        # GALAS
        # ==========================================
        gala1, _ = Gala.objects.get_or_create(nom="Gala d'hiver", defaults={
            'date': date(2026, 2, 14), 'lieu': "Centre Georges-Vézina", 'ville': "Chicoutimi",
            'description': "Premier gala de la saison, ouvert par nos meilleurs espoirs.",
            'organisateur': club1, 'statut': 'termine', 'capacite_max': 500
        })
        gala2, _ = Gala.objects.get_or_create(nom="Gala du printemps", defaults={
            'date': date(2026, 11, 20), 'lieu': "Centre Vidéotron", 'ville': "Québec",
            'description': "Une carte relevée avec plusieurs affrontements de catégories moyennes.",
            'organisateur': club3, 'statut': 'a_venir', 'capacite_max': 800
        })
        gala3, _ = Gala.objects.get_or_create(nom="Gala des champions", defaults={
            'date': date(2027, 1, 15), 'lieu': "Centre Bell", 'ville': "Montréal",
            'description': "Le plus grand événement de l'année, avec un main event très attendu.",
            'organisateur': club2, 'statut': 'a_venir', 'capacite_max': 1200
        })

        # ==========================================
        # COMBATS
        # ==========================================
        def creer_combat(gala, rouge, bleu, categorie, type_combat, nb_rounds, ordre,
                          arb_p, arb_a, resultat='non_joue', methode=None):
            Combat.objects.get_or_create(
                gala=gala, boxeur_rouge=rouge, boxeur_bleu=bleu, categorie=categorie, ordre=ordre,
                defaults={
                    'type_combat': type_combat, 'nb_rounds': nb_rounds,
                    'arbitre_principal': arb_p, 'arbitre_assistant': arb_a,
                    'resultat': resultat, 'methode': methode
                }
            )

        # --- Gala 1 : TERMINÉ (4 combats, résultats remplis) ---
        creer_combat(gala1, mouche_a, mouche_b, cat["Poids mouche"], 'preliminaire', 4, 1,
                     arb1, arb2, 'victoire_rouge', 'decision')
        creer_combat(gala1, coq_a, coq_b, cat["Poids coq"], 'preliminaire', 4, 2,
                     arb2, arb1, 'victoire_bleu', 'tko')
        creer_combat(gala1, plume_a, plume_b, cat["Poids plume"], 'co_main', 8, 3,
                     arb1, arb2, 'nul', None)
        creer_combat(gala1, leger_a, leger_b, cat["Poids léger"], 'main_event', 10, 4,
                     arb2, arb1, 'victoire_rouge', 'ko')

        # --- Gala 2 : À VENIR (6 combats, pas encore joués) ---
        creer_combat(gala2, mimoyen_a, mimoyen_b, cat["Poids mi-moyen"], 'preliminaire', 4, 1, arb1, arb2)
        creer_combat(gala2, moyen_a, moyen_b, cat["Poids moyen"], 'preliminaire', 4, 2, arb2, arb1)
        creer_combat(gala2, milourd_a, milourd_b, cat["Poids mi-lourd"], 'preliminaire', 6, 3, arb1, arb2)
        creer_combat(gala2, leger_b, leger_c, cat["Poids léger"], 'preliminaire', 6, 4, arb2, arb1)
        creer_combat(gala2, mimoyen_b, mimoyen_c, cat["Poids mi-moyen"], 'co_main', 8, 5, arb1, arb2)
        creer_combat(gala2, lourd_a, lourd_b, cat["Poids lourd"], 'main_event', 10, 6, arb2, arb1)

        # --- Gala 3 : À VENIR (7 combats, pas encore joués) ---
        creer_combat(gala3, mouche_a, mouche_b, cat["Poids mouche"], 'preliminaire', 4, 1, arb1, arb2) 
        creer_combat(gala3, plume_b, plume_a, cat["Poids plume"], 'preliminaire', 4, 2, arb2, arb1)
        creer_combat(gala3, leger_a, leger_c, cat["Poids léger"], 'preliminaire', 6, 3, arb1, arb2)
        creer_combat(gala3, mimoyen_a, mimoyen_c, cat["Poids mi-moyen"], 'preliminaire', 6, 4, arb2, arb1)
        creer_combat(gala3, moyen_b, moyen_a, cat["Poids moyen"], 'co_main', 8, 5, arb1, arb2)
        creer_combat(gala3, milourd_b, milourd_a, cat["Poids mi-lourd"], 'co_main', 8, 6, arb2, arb1)
        creer_combat(gala3, lourd_b, lourd_a, cat["Poids lourd"], 'main_event', 12, 7, arb1, arb2)

        # ==========================================
        # UTILISATEURS DE TEST + BILLETS
        # ==========================================
        user1, created = User.objects.get_or_create(username="jdupont", defaults={'email': 'jdupont@test.com'})
        if created:
            user1.set_password("test1234")
            user1.save()

        user2, created = User.objects.get_or_create(username="mleclerc", defaults={'email': 'mleclerc@test.com'})
        if created:
            user2.set_password("test1234")
            user2.save()

        Billet.objects.get_or_create(gala=gala2, utilisateur=user1, type_place='gradin', defaults={'prix': 35.00})
        Billet.objects.get_or_create(gala=gala2, utilisateur=user2, type_place='vip', defaults={'prix': 120.00})
        Billet.objects.get_or_create(gala=gala3, utilisateur=user1, type_place='ringside', defaults={'prix': 85.00})

        self.stdout.write(self.style.SUCCESS(
            "Données de test créées : 3 clubs, 8 catégories, 18 boxeurs, 2 arbitres, "
            "3 galas (4+6+7 combats), 2 utilisateurs, 3 billets."
        ))