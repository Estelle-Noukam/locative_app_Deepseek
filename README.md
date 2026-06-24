Application web pour la gestion de biens immobiliers avec Flask et PostgreSQL.

## Installation et lancement

```bash
## Démarrer l'application
docker-compose up --build

## Accéder à l'application
http://localhost:5000
Comptes par défaut
Rôle	Email	Mot de passe
Administrateur	admin@example.com	admin123
Fonctionnalités
Gestion des utilisateurs
Création de comptes (inscription)

Connexion / Déconnexion

3 rôles : Administrateur, Propriétaire, Locataire

Profil utilisateur modifiable

Gestion des propriétés
Création, modification, suppression de logements

Recherche par ville et disponibilité

Gestion des annonces

Gestion des baux
Création de contrats de location

Suivi des baux actifs/terminés

Association propriétaire-locataire

Paiements
Suivi des loyers

Enregistrement des paiements

Statut : en attente, payé, en retard

Réclamations
Demandes de maintenance

Suivi des réclamations

Statut : en attente, en cours, résolu

Demandes de location
Les locataires peuvent faire des demandes

Les propriétaires approuvent ou rejettent

Tableau de bord
Statistiques globales (admin)

Vue propriétaire : ses biens et demandes

Vue locataire : logements disponibles et paiements

API RESTful
Accès aux données via API

Endpoints pour toutes les entités

Commandes utiles
bash
docker-compose up -d          # Démarrer en arrière-plan
docker-compose down           # Arrêter
docker-compose down -v        # Réinitialiser (supprime les données)
docker-compose logs -f        # Voir les logs
docker-compose logs web       # Voir les logs du backend
Structure du projet
text
locative_app/
├── backend/
│   ├── app.py              # Application principale
│   ├── requirements.txt    # Dépendances Python
│   └── templates/          # Templates HTML
├── Dockerfile              # Configuration Docker
└── docker-compose.yml      # Orchestration des services
Dépannage
Port déjà utilisé
bash

## Modifier les ports dans docker-compose.yml
services:
  db:
    ports:
      - "5433:5432"  # PostgreSQL
  web:
    ports:
      - "5001:5000"  # Web
Réinitialiser la base de données
bash
docker-compose down -v
docker-compose up --build
Routes API principales
Route	Description
/api/users	Gestion des utilisateurs (admin)
/api/properties	Gestion des propriétés
/api/leases	Gestion des baux
/api/payments	Gestion des paiements
/api/complaints	Gestion des réclamations
/api/rental-requests	Gestion des demandes
/api/stats	Statistiques (admin)
Technologies
Backend : Python 3.11 + Flask

Base de données : PostgreSQL 15

ORM : SQLAlchemy

Authentification : Flask-Login

Frontend : Bootstrap 5 + jQuery

Containerisation : Docker & Docker Compose
