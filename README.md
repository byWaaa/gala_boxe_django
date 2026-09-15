# 🥊 Gala Boxe — Gestion de gala de boxe anglaise

Application web développée avec **Django** permettant de gérer l'organisation de galas de boxe anglaise : clubs, boxeurs, combats et billetterie en ligne.

> Projet réalisé dans le cadre du cours **Programmation web et sécurité (420-E60-CH)**.

---

## 📋 Description

Gala Boxe est une application transactionnelle qui simule la gestion complète d'un événement de boxe anglaise, du côté organisateur comme du côté public :

- **Le public** peut consulter les galas à venir, les résultats passés, les fiches des boxeurs et leurs statistiques.
- **Les utilisateurs inscrits** peuvent réserver et acheter des billets pour assister aux galas.
- **Les organisateurs** (comptes staff) gèrent l'ensemble des données : clubs, boxeurs, arbitres, galas et combats, avec un suivi complet des modifications et suppressions.

L'application respecte l'architecture **MVT** (Model–View–Template) de Django et utilise une base de données relationnelle **SQLite** avec plusieurs modèles reliés entre eux (relations 1-N et N-N).

---

## ✨ Fonctionnalités

### Côté public
- Consultation des galas (à venir, en cours, terminés)
- Fiches détaillées des boxeurs (statistiques calculées dynamiquement : victoires, défaites, nuls)
- Détail des combats par gala (résultat, méthode, catégorie de poids)
- Page d'accueil avec prochains galas, résumé du dernier gala et statistiques globales

### Côté utilisateur connecté
- Inscription / connexion / déconnexion
- Achat et réservation de billets (gestion de la capacité maximale par gala)
- Consultation de ses propres billets

### Côté organisateur (staff)
- Gestion CRUD complète : clubs, boxeurs, arbitres, galas, combats
- Formulaires avec validations métier (ex. : un boxeur ne peut pas combattre lui-même, les deux boxeurs doivent être de la même catégorie de poids, un boxeur avec des combats ne peut pas être supprimé)
- Suppression de combat avec justification obligatoire, conservée dans un historique
- Interface d'administration Django personnalisée (filtres, recherche)

---

## 🛠️ Stack technique

| Composant | Technologie |
|---|---|
| Langage | Python 3.x |
| Framework web | Django (dernière version stable) |
| Base de données | SQLite |
| Front-end | HTML5, Bootstrap 5, CSS |
| Authentification | Système natif Django (`django.contrib.auth`) |

---

## 🗂️ Modèles de données

- **Club** — clubs de boxe (nom, ville, date de fondation, nombre de combattants, logo)
- **CategoriePoids** — catégories officielles de poids en boxe anglaise
- **Boxeur** — profil d'un boxeur, rattaché à un club et une catégorie de poids
- **Arbitre** — arbitres pouvant officier sur plusieurs combats
- **Gala** — événement organisé par un club, avec capacité de billets
- **Combat** — affrontement entre deux boxeurs lors d'un gala (résultat, méthode, rounds, arbitres)
- **Billet** — réservation d'un utilisateur pour un gala (relation N-N avec attributs)
- **HistoriqueSuppression** — traçabilité des combats supprimés et de leur justification

Schéma des relations détaillé disponible dans [`plan-projet-gala-boxe.md`](./plan-projet-gala-boxe.md).

---

## 🚀 Installation

### Prérequis
- Python 3.x installé
- `pip` et `venv`

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/TON-USERNAME/gala-boxe-django.git
cd gala-boxe-django

# 2. Créer et activer un environnement virtuel
python -m venv .venv
source .venv/bin/activate      # Sur Windows : .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. Charger les données de départ (fixtures)
python manage.py loaddata gala/fixtures/donnees_initiales.json

# 6. Créer un compte administrateur
python manage.py createsuperuser

# 7. Lancer le serveur de développement
python manage.py runserver
```

L'application est ensuite accessible sur `http://127.0.0.1:8000/`
L'interface d'administration sur `http://127.0.0.1:8000/admin/`

---

## 📁 Structure du projet

```
gala_boxe/
├── manage.py
├── requirements.txt
├── README.md
├── gala_boxe/          # Configuration du projet
│   ├── settings.py
│   └── urls.py
├── gala/                # Application principale
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/gala/
│   ├── static/gala/
│   └── fixtures/
└── media/               # Fichiers uploadés (non versionné)
```

---

## 🔒 Sécurité

- Contrôle d'accès basé sur les permissions (`@login_required`, `@staff_member_required`)
- Filtrage systématique des objets par utilisateur propriétaire (pas seulement par identifiant d'URL)
- Prix des billets calculés côté serveur (jamais transmis par le client)
- Validation des formulaires côté serveur (champs explicitement listés, jamais `__all__`)
- `DEBUG = False` en environnement de production, `SECRET_KEY` non exposée dans le dépôt

---

## 👤 Auteur

**Monaim** — Étudiant en Techniques de l'informatique (Développement d'applications), HEPH Condorcet
