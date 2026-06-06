# Ymmo — Plateforme de gestion immobilière (Partie DEV)

PAR : NJUNDOM STELLA & KLARA PERIC 
    B2 CYBERSECURITE & B2 INFORMATIQUE

Application web de gestion d'**achat et de vente de biens immobiliers** pour le groupe
fictif **Ymmo**, développée en **Python (Flask)** avec une base de données **MySQL**.

Ce dépôt couvre **uniquement la partie DEV** du projet INFRA & DEV :
site web + base de données + module d'analyse de données.

---
## Sommaire
1. [Fonctionnalités](#fonctionnalités)
2. [Architecture Globale](#architecture-globale)
3. [Détail Fichier par Fichier](#détail-fichier-par-fichier)
4. [Sécurité et Conformité](#sécurité-et-conformité)
5. [Compétences du Brief Couvertes](#compétences-du-brief-couvertes)
6. [Prérequis et Dépendances](#prérequis-et-dépendances)
7. [Installation pas à pas](#installation-pas-à-pas)
8. [Configuration de la Base de Données](#configuration-de-la-base-de-données)
9. [Lancement et Jeu de Test](#lancement-et-jeu-de-test)
10. [Modèle de Données (Relationnel)](#modèle-de-données-relationnel)

---

## Fonctionnalités

- **Catalogue de biens** avec moteur de recherche multi-critères (ville, type, budget max, nombre de pièces)
- **Détail d'un bien** (prix au m², caractéristiques, agent).
- **Authentification** (inscription, connexion, déconnexion) avec mots de passe **hachés**.
- **Gestion des rôles** : client, agent, administrateur.
- **CRUD des biens** réservé aux agents (créer, modifier, supprimer).
- **Offres d'achat** déposées par les clients.
- **Tableau de bord d'analyse de données** (pandas) : prix moyen, statistiques par ville,
  biens populaires, zones intéressantes à l'achat.
- Interface **responsive** (mobile / tablette / desktop) et **accessible** (HTML sémantique, labels, lien d'évitement, focus visible, contrastes)
- **Fiches descriptives riches** calculant automatiquement des indicateurs clés (prix au m², caractéristiques, agent référent).
- **Gestion des offres** : Dépôt d'offres d'achat interactives par les clients connectés.

## Architecture Globale

L'application implémente une architecture découplée en couches (**Pattern : Models → Services → Routes → Templates**), garantissant le strict respect des critères d'évaluation du brief client :

## Architecture du projet

```
ymmo/
├── run.py                      # Point d'entrée (python run.py)
├── seed.py                     # Initialise la BDD + données de démo
├── requirements.txt            # Dépendances Python
├── .env.example                # Modèle de variables d'environnement
├── .gitignore
├── README.md
└── app/
    ├── __init__.py             # Application factory (create_app)
    ├── config.py               # Configuration (lecture du .env)
    ├── extensions.py           # Instances db, login_manager
    ├── models/                 # Couche données (POO) — 1 classe = 1 table
    │   ├── base.py             # Mixin commun (DRY)
    │   ├── user.py             # Utilisateur + rôles
    │   ├── property.py         # Bien immobilier
    │   └── transaction.py      # Offre d'achat / vente
    ├── services/               # Logique métier (SOLID - responsabilité unique)
    │   ├── property_service.py
    │   └── analytics_service.py
    ├── routes/                 # Contrôleurs (blueprints Flask)
    │   ├── auth.py
    │   ├── properties.py
    │   ├── analytics.py
    │   └── decorators.py       # Contrôle d'accès par rôle
    ├── templates/              # Vues HTML (Jinja2)
    │   ├── base.html
    │   ├── auth/  properties/  analytics/  errors/
    └── static/
        └── css/style.css       # Style responsive et accessible
```

### 💡 Justifications de l'ingénierie logicielle
* **Principes SOLID (Responsabilité Unique)** : Les fichiers de `routes/` (contrôleurs) s'occupent uniquement de la tuyauterie HTTP. Toute la logique algorithmique, les traitements lourds (Pandas) et la génération de documents sont délégués à la couche `services/`.
* **Principe DRY (Don't Repeat Yourself)** : La classe `BaseMixin` dans `base.py` centralise les propriétés communes (Identifiants, Timestamps) héritées par tous les modèles de données de l'application, évitant la duplication de code.

---

## Détail Fichier par Fichier

### Racine du Projet (`ymmo/`)

* **`run.py`** : Le point d'entrée de l'application web. C'est le fichier exécuté pour démarrer le serveur de développement local Flask. Il appelle l'Application Factory (`create_app`) pour initialiser l'instance.
* **`seed.py`** : Script d'automatisation et d'injection de données. Il réinitialise complètement le schéma de la base de données MySQL et injecte un jeu de test réaliste (comptes utilisateurs de démo, annonces et transactions d'exemple).
* **`requirements.txt`** : Manifeste listant l'ensemble des dépendances et bibliothèques Python externes nécessaires au bon fonctionnement et à la stabilité du projet (Flask, Pandas, SQLAlchemy, etc.).
* **`.env.example`** : Modèle de configuration des variables d'environnement. Il sert de guide pour configurer les accès locaux à la base de données sans stocker d'identifiants sensibles directement dans le code source.
* **`.gitignore`** : Fichier d'exclusion pour Git. Il empêche le suivi et la publication de fichiers inutiles ou confidentiels, comme le dossier de l'environnement virtuel (`venv/`) ou le fichier `.env` actif

### Le Cœur Applicatif (`app/`)

* **`app/__init__.py`** : Implémente le pattern *Application Factory*. Il configure l'application Flask, initialise les extensions de base de données, gère les protections de sécurité globales et connecte les différents contrôleurs (Blueprints).
* **`app/config.py`** : Charge et structure les variables de configuration de l'application. Il lit les données du fichier `.env` pour les convertir en propriétés système exploitables par Flask.
* **`app/extensions.py`** : Déclare et isole les instances globales des outils tiers sous forme de Singletons (comme l'ORM `SQLAlchemy` et le gestionnaire de sessions `Flask-Login`) avant leur attachement à l'application.

### La Couche Modèles (`app/models/`) — *Garant de la POO Advanced*

* **`app/models/base.py`** : Contient un Mixin abstrait regroupant les propriétés universelles (Identifiants uniques `id`, horodatages système). Il permet d'appliquer le principe DRY en évitant la duplication de colonnes communes.
* **`app/models/user.py`** : Représente la table `users` en base de données. Il stocke les informations de profil (email, rôle métier) et encapsule la logique de sécurité (salage et hachage cryptographique des mots de passe).
* **`app/models/property.py`** : Modélise la table `properties`. Il structure l'ensemble des caractéristiques physiques et financières des annonces immobilières et porte la clé étrangère le liant à l'agent responsable.
* **`app/models/transaction.py`** : Représente la table pivot `transactions`. Elle enregistre l'historique, les montants et les statuts des offres d'achat formulées, créant une passerelle relationnelle stricte entre un client et un bien.

### La Couche Métier (`app/services/`) — *Respect du principe SOLID*

* **`app/services/property_service.py`** : Gère l'ensemble de la logique métier liée au catalogue. Il centralise les actions de création, d'édition, de suppression des fiches et l'exécution des filtres de recherche.
* **`app/services/analytics_service.py`** : Le moteur décisionnel du projet. Il exécute des requêtes SQL d'agrégation complexes, charge les résultats dans des structures de données Pandas pour extraire des statistiques de marché, et pilote l'algorithme d'édition et de mise en page native du rapport exportable en format PDF.

### La Couche Contrôleurs (`app/routes/`)

* **`app/routes/auth.py`** : Intercepte les requêtes HTTP liées aux processus d'authentification. Il pilote l'affichage des formulaires, la validation des accès et l'ouverture ou la fermeture des sessions de navigation.
* **`app/routes/properties.py`** : Gère la navigation sur le catalogue immobilier, la consultation détaillée des fiches de biens et la réception des formulaires de soumission d'offres.
* **`app/routes/analytics.py`** : Point d'accès au tableau de bord stratégique. Il transmet les métriques calculées à la vue et distribue le flux binaire du fichier PDF généré lors d'une demande de téléchargement.
* **`app/routes/decorators.py`** : Centralise la sécurité basée sur les rôles (RBAC). Il contient les décorateurs personnalisés qui filtrent les requêtes HTTP en amont pour bloquer toute tentative d'accès non autorisé (Erreur 403).

### La Couche Vues et Présentation (`app/templates/` & `app/static/`)

* **`app/templates/base.html`** : Squelette HTML5 sémantique global partagé par toutes les pages du site. Il intègre l'ossature d'accessibilité (repères WCAG, structures de navigation au clavier).
* **`app/templates/auth/`** : Regroupe les interfaces utilisateurs d'authentification (connexion et inscription).
* **`app/templates/properties/`** : Contient les templates d'affichage du catalogue, de consultation détaillée et les formulaires d'édition des biens.
* **`app/templates/analytics/`** : Interface du tableau de bord affichant les analyses statistiques Pandas et le module de téléchargement de rapport.
* **`app/templates/errors/`** : Contient les pages de routage des erreurs système (403, 404) pour garantir une expérience utilisateur fluide en cas d'anomalie.
* **`app/static/css/style.css`** : Feuille de style CSS native. Elle structure le design visuel, assure la mise en conformité des contrastes de couleurs et gère le comportement adaptatif (Responsive Design) de l'interface sur mobile, tablette et desktop.

---

## Sécurité et Conformité

### Sécurité Applicative (OWASP Top 10)
- **Hachage Cryptographique** : Les mots de passe des utilisateurs ne sont jamais stockés en clair. L'application utilise l'algorithme robuste **Scrypt** via la bibliothèque `Werkzeug` pour le salage et le hachage systématique.
- **Contrôle d'Accès Basé sur les Rôles (RBAC)** : Les actions sensibles (CRUD du catalogue, Dashboard d'analyse, Exports) sont verrouillées au niveau du serveur par des décorateurs personnalisés (`@agent_required`, `@admin_required`). Toute tentative de modification d'URL par un utilisateur non autorisé est immédiatement interceptée et rejetée (Code HTTP 403).
- **Sécurisation de la Persistance** : Utilisation de l'ORM SQLAlchemy avec requêtes paramétrées natives pour éliminer structurellement tout risque d'**Injection SQL**.
- **Variables d'environnement** : Isolation complète des données sensibles (clés privées, identifiants de production) hors du code source via le fichier `.env`.

### Accessibilité et Qualité Web (Normes RGAA / WCAG)
L'interface utilisateur a été conçue pour offrir une navigation inclusive :
- **Sémantique HTML5 stricte** (`<main>`, `<nav>`, `<header>`, `<section>`) pour assurer une compatibilité parfaite avec les lecteurs d'écran.
- **Navigation au clavier complète** (gestion logique du focus visible, ordre des tabulations préservé)
- **Rapports de contraste élevés** conformes aux exigences AA pour une lisibilité optimale sur tous les terminaux.

---

## Compétences du Brief Couvertes

| Exigence du cahier des charges | Emplacement dans l'implémentation |
| :--- | :--- |
| **Architecture backend orientée services** | Isolé dans la couche `app/services/` |
| **Concepts de la POO avancée** | Héritage, encapsulation et polymorphisme dans `app/models/` |
| **Requêtes SQL avancées** | Agrégations et jointures relationnelles complexes dans `analytics_service.py` |
| **Analyse statistique et reporting** | Dataframes `Pandas` et moteur d'export PDF algorithmique |
| **Interfaces adaptatives (Responsive)** | Grilles fluides, Flexbox et Media Queries dans `app/static/css/style.css` |

---

## Prérequis et Dépendances

- **Python 3.10 ou supérieur**
- **MySQL 8.0** ou instance MariaDB équivalente
- Dépendances majeures : `Flask`, `Flask-SQLAlchemy`, `Flask-Login`, `pandas`, `fpdf2`, `python-dotenv`.

---

## Installation pas à pas

```bash
# 1. Se placer à la racine du projet
cd ymmo

# 2. Initialiser l'environnement virtuel isolé
python -m venv venv

# 3. Activer l'environnement
# Windows (cmd/PowerShell) :
venv\Scripts\activate
# macOS / Linux :
source venv/bin/activate

# 4. Installer le manifeste des dépendances
pip install -r requirements.txt

# 5. Déployer le fichier de configuration locale
# Windows : copy .env.example .env
# macOS/Linux : cp .env.example .env
```

## Configuration de la Base de donnéesj

### 1. Créer la base de données

Connecte-toi à MySQL (en ligne de commande ou via Workbench) et exécute :

```sql
CREATE DATABASE ymmo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

> Tu n'as **pas besoin de créer les tables à la main** : le script `seed.py` les crée
> automatiquement via SQLAlchemy (`db.create_all()`).

### 2. (Optionnel) Créer un utilisateur dédié

```sql
CREATE USER 'ymmo_user'@'localhost' IDENTIFIED BY 'TonMotDePasse';
GRANT ALL PRIVILEGES ON ymmo.* TO 'ymmo_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Renseigner le fichier `.env`

```env
DB_USER=root            # ou ymmo_user
DB_PASSWORD=TonMotDePasse
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ymmo
SECRET_KEY=mets-une-longue-chaine-aleatoire
```

---

## Lancement de l'application

```bash
# 1. Créer les tables + insérer les données de démonstration
python seed.py

# 2. Démarrer le serveur de développement
python run.py
```

L'application est accessible sur **http://127.0.0.1:5000**

---

## Comptes de démonstration

Créés automatiquement par `seed.py` :

| Rôle   | Email            | Mot de passe |
|--------|------------------|--------------|
| Admin  | admin@ymmo.fr    | admin123     |
| Agent  | agent@ymmo.fr    | agent123     |
| Client | client@ymmo.fr   | client123    |

> Connecte-toi en **agent** pour publier des biens et accéder au **tableau de bord d'analyse**.
> Connecte-toi en **client** pour faire une **offre d'achat**.

---

## Modèle de données

L'intégrité de la persistance repose sur trois tables maîtresses hautement normalisées :

- **users** : Registre des comptes utilisateurs. Stocke le rôle métier de l'utilisateur (client, agent, admin) et ses identifiants sécurisés (mots de passe hachés).
- **properties** : Inventaire des biens immobiliers indexés par ville, prix, surface et type. Chaque bien est sémantiquement rattaché à l'agent responsable qui en a la charge.
- **transactions** : Table pivot enregistrant l'ensemble des propositions financières formulées par les clients sur les biens du catalogue, avec cycle de validation des statuts (En attente, Acceptée, Refusée).

Relations :
- Un **agent** supervise ou publie Plusieurs Biens (properties) donc (Relation 1:N)
- Un **client** soumet Plusieurs Offres (transactions) donc (Relation 1:N)
- Un **bien** peut collecter Plusieurs Propositions (transactions) donc Relation 1:N
---