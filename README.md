Application web complète pour la gestion de biens immobiliers avec Flask et PostgreSQL.

---

## 🚀 Installation et lancement

```bash
# Cloner et lancer
docker-compose up --build

# Accéder à l'application
http://localhost:5000
🔑 Comptes par défaut
Rôle	Email	Mot de passe
👑 Administrateur	admin@example.com	admin123
👤 Propriétaire	Créer via inscription	-
👤 Locataire	Créer via inscription	-
✨ Fonctionnalités
👥 Gestion des utilisateurs
Création de comptes (inscription)

Connexion / Déconnexion

3 rôles : Administrateur, Propriétaire, Locataire

Profil utilisateur modifiable

🏢 Gestion des propriétés
Création, modification, suppression de logements

Recherche par ville et disponibilité

Gestion des annonces

📄 Gestion des baux
Création de contrats de location

Suivi des baux (actifs/terminés)

Association propriétaire-locataire

💰 Paiements
Suivi des loyers

Enregistrement des paiements

Statut : en attente, payé, en retard

🔧 Réclamations
Demandes de maintenance

Suivi des réclamations

Statut : en attente, en cours, résolu

📨 Demandes de location
Les locataires font des demandes

Les propriétaires approuvent ou rejettent

📊 Tableau de bord
Admin : Statistiques globales

Propriétaire : Ses biens et demandes

Locataire : Logements disponibles et paiements

🔌 API RESTful
Accès aux données via API

Endpoints pour toutes les entités

📂 Structure du projet
text
locative_app/
├── backend/
│   ├── app.py              # Application principale
│   ├── requirements.txt    # Dépendances Python
│   └── templates/          # Templates HTML
├── Dockerfile              # Configuration Docker
└── docker-compose.yml      # Orchestration des services
🛠️ Technologies
Composant	Technologie
Backend	Python 3.11 + Flask
Base de données	PostgreSQL 15
ORM	SQLAlchemy
Authentification	Flask-Login
Frontend	Bootstrap 5 + jQuery
Containerisation	Docker & Docker Compose
📡 Routes API
Route	Description	Accès
/api/users	Gestion utilisateurs	Admin
/api/properties	Gestion propriétés	Tous
/api/leases	Gestion baux	Tous
/api/payments	Gestion paiements	Tous
/api/complaints	Gestion réclamations	Tous
/api/rental-requests	Gestion demandes	Tous
/api/stats	Statistiques	Admin
🐳 Commandes Docker
bash
docker-compose up -d          # Démarrer en arrière-plan
docker-compose down           # Arrêter
docker-compose down -v        # Réinitialiser (supprime les données)
docker-compose logs -f        # Voir les logs
docker-compose logs web       # Voir les logs du backend
docker-compose restart web    # Redémarrer le backend
🔧 Dépannage
Port déjà utilisé
bash
# Modifier les ports dans docker-compose.yml
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
Voir les erreurs
bash
docker-compose logs web
docker-compose logs db
